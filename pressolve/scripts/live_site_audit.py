#!/usr/bin/env python3
"""Run a bounded, read-only public website audit and emit JSON."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import ssl
import sys
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


SCHEMA = "pressolve-live-audit/v1"
USER_AGENT = "Pressolve-Live-Audit/2.1 (+https://github.com/jmqbataller/pressolve)"
MAX_BODY = 1_500_000
MAX_SITEMAP = 500_000
SKIP_PATH = re.compile(
    r"/(?:wp-admin|wp-login\.php|xmlrpc\.php|cart|checkout|my-account|logout|"
    r"password-reset|lost-password)(?:/|$)",
    re.I,
)
SKIP_EXTENSION = re.compile(r"\.(?:avif|css|gif|ico|jpe?g|js|json|mp3|mp4|pdf|png|svg|webm|webp|xml|zip)$", re.I)


class AuditError(RuntimeError):
    """Expected target or network error."""


class PageFacts(HTMLParser):
    """Collect passive, non-content website facts from HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.lang: str | None = None
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None
        self.links: list[str] = []
        self.resources: list[str] = []
        self.h1_count = 0
        self.h2_count = 0
        self.images = 0
        self.images_without_alt = 0
        self.forms = 0
        self.generator: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html" and values.get("lang"):
            self.lang = values["lang"].strip()
        elif tag == "title":
            self.in_title = True
        elif tag == "meta":
            key = (values.get("name") or values.get("property") or values.get("http-equiv") or "").lower()
            content = values.get("content", "").strip()
            if key and key not in self.meta:
                self.meta[key] = content
            if key == "generator":
                self.generator = content
        elif tag == "link":
            href = values.get("href", "").strip()
            rel = {part.lower() for part in values.get("rel", "").split()}
            if href:
                self.resources.append(href)
            if "canonical" in rel and href:
                self.canonical = href
        elif tag == "a":
            href = values.get("href", "").strip()
            if href:
                self.links.append(href)
        elif tag in {"script", "iframe", "source", "video", "audio"}:
            source = values.get("src", "").strip()
            if source:
                self.resources.append(source)
        elif tag == "img":
            self.images += 1
            if "alt" not in values:
                self.images_without_alt += 1
            source = values.get("src", "").strip()
            if source:
                self.resources.append(source)
        elif tag == "form":
            self.forms += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "h2":
            self.h2_count += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def require_global_addresses(addresses: set[str]) -> None:
    if not addresses:
        raise AuditError("The hostname did not resolve to an IP address")
    blocked = [value for value in addresses if not ipaddress.ip_address(value).is_global]
    if blocked:
        raise AuditError("Private, local, reserved, or non-public network targets are not allowed")


def validate_public_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    if parsed.scheme.lower() not in {"http", "https"}:
        raise AuditError("Use a complete http:// or https:// URL")
    if parsed.username or parsed.password:
        raise AuditError("URLs containing credentials are not allowed")
    if not parsed.hostname:
        raise AuditError("The URL has no hostname")
    hostname = parsed.hostname.encode("idna").decode("ascii").rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith((".localhost", ".local", ".internal")):
        raise AuditError("Local and internal hostnames are not allowed")
    try:
        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    except ValueError as error:
        raise AuditError("The URL contains an invalid port") from error
    try:
        infos = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise AuditError(f"The hostname could not be resolved: {error}") from error
    require_global_addresses({item[4][0] for item in infos})
    return urlunsplit((parsed.scheme.lower(), parsed.netloc, parsed.path or "/", parsed.query, ""))


class SafeRedirectHandler(HTTPRedirectHandler):
    def __init__(self) -> None:
        super().__init__()
        self.chain: list[str] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        safe_url = validate_public_url(newurl)
        self.chain.append(safe_url)
        if len(self.chain) > 5:
            raise AuditError("More than five redirects were encountered")
        return super().redirect_request(req, fp, code, msg, headers, safe_url)


def decode_body(body: bytes, content_type: str) -> str:
    match = re.search(r"charset=([A-Za-z0-9._-]+)", content_type, re.I)
    encodings = [match.group(1)] if match else []
    encodings.extend(["utf-8", "latin-1"])
    for encoding in encodings:
        try:
            return body.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return body.decode("utf-8", errors="replace")


class Fetcher:
    def __init__(self, timeout: float) -> None:
        self.timeout = timeout
        self.redirects = SafeRedirectHandler()
        self.opener = build_opener(self.redirects)

    def get(self, url: str, limit: int = MAX_BODY) -> dict[str, Any]:
        safe_url = validate_public_url(url)
        self.redirects.chain = []
        request = Request(
            safe_url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/json,application/xml,text/plain;q=0.9,*/*;q=0.5"},
            method="GET",
        )
        started = time.monotonic()
        try:
            response = self.opener.open(request, timeout=self.timeout)
        except HTTPError as error:
            response = error
        except (URLError, TimeoutError, OSError, AuditError) as error:
            return {
                "requested_url": safe_url,
                "final_url": safe_url,
                "status": None,
                "error": str(getattr(error, "reason", error)),
                "redirects": list(self.redirects.chain),
                "headers_ms": None,
                "total_ms": round((time.monotonic() - started) * 1000),
                "headers": {},
                "body": b"",
                "truncated": False,
            }

        headers_ms = round((time.monotonic() - started) * 1000)
        try:
            body = response.read(limit + 1)
        except OSError:
            body = b""
        headers = {key.lower(): value for key, value in response.headers.items()}
        final_url = response.geturl()
        try:
            validate_public_url(final_url)
        except AuditError as error:
            raise AuditError(f"Unsafe final redirect target: {error}") from error
        return {
            "requested_url": safe_url,
            "final_url": final_url,
            "status": int(response.getcode()),
            "error": None,
            "redirects": list(self.redirects.chain),
            "headers_ms": headers_ms,
            "total_ms": round((time.monotonic() - started) * 1000),
            "headers": headers,
            "body": body[:limit],
            "truncated": len(body) > limit,
        }


def parse_html(result: dict[str, Any]) -> PageFacts | None:
    content_type = result["headers"].get("content-type", "")
    body = result.get("body", b"")
    if not body or ("html" not in content_type.lower() and b"<html" not in body[:1000].lower()):
        return None
    parser = PageFacts()
    try:
        parser.feed(decode_body(body, content_type))
    except Exception:
        return None
    return parser


def normalize_link(base: str, raw: str) -> str | None:
    if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None
    absolute = urlsplit(urljoin(base, raw))
    if absolute.scheme.lower() not in {"http", "https"} or not absolute.hostname:
        return None
    return urlunsplit((absolute.scheme.lower(), absolute.netloc, absolute.path or "/", absolute.query, ""))


def normalized_host(url: str) -> str:
    return (urlsplit(url).hostname or "").lower().removeprefix("www.")


def same_site(left: str, right: str) -> bool:
    return normalized_host(left) == normalized_host(right)


def display_url(url: str) -> str:
    parsed = urlsplit(url)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", "", ""))


def crawlable(url: str, origin: str, disallowed: list[str]) -> bool:
    parsed = urlsplit(url)
    if not same_site(url, origin) or parsed.query or SKIP_PATH.search(parsed.path) or SKIP_EXTENSION.search(parsed.path):
        return False
    return not any(rule and parsed.path.startswith(rule) for rule in disallowed)


def robots_rules(text: str) -> tuple[list[str], list[str]]:
    disallowed: list[str] = []
    sitemaps: list[str] = []
    active = False
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = (part.strip() for part in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            active = value in {"*", "Pressolve-Live-Audit"}
        elif key == "disallow" and active and value.startswith("/"):
            disallowed.append(value)
        elif key == "sitemap" and value.lower().startswith(("http://", "https://")):
            sitemaps.append(value)
    return sorted(set(disallowed)), list(dict.fromkeys(sitemaps))


def sitemap_locations(text: str, base: str) -> list[str]:
    locations: list[str] = []
    for value in re.findall(r"<loc\b[^>]*>\s*(.*?)\s*</loc>", text, flags=re.I | re.S):
        clean = re.sub(r"\s+", "", value).replace("&amp;", "&")
        link = normalize_link(base, clean)
        if link and same_site(link, base):
            locations.append(link)
        if len(locations) >= 100:
            break
    return list(dict.fromkeys(locations))


def page_priority(url: str) -> tuple[int, int, str]:
    path = urlsplit(url).path.lower()
    keywords = ("about", "service", "contact", "shop", "product", "blog", "news", "property", "listing", "privacy")
    rank = next((index for index, word in enumerate(keywords) if word in path), len(keywords))
    return rank, path.count("/"), path


def resource_clues(base: str, facts: PageFacts | None) -> tuple[list[str], list[str], int]:
    if not facts:
        return [], [], 0
    resources = [normalize_link(base, item) for item in facts.resources]
    clean = [item for item in resources if item]
    plugins: set[str] = set()
    themes: set[str] = set()
    mixed = 0
    for item in clean:
        path = urlsplit(item).path
        plugin = re.search(r"/wp-content/plugins/([^/]+)/", path, re.I)
        theme = re.search(r"/wp-content/themes/([^/]+)/", path, re.I)
        if plugin:
            plugins.add(plugin.group(1).lower())
        if theme:
            themes.add(theme.group(1).lower())
        if urlsplit(base).scheme == "https" and urlsplit(item).scheme == "http":
            mixed += 1
    return sorted(plugins), sorted(themes), mixed


def page_summary(result: dict[str, Any], origin: str) -> dict[str, Any]:
    facts = parse_html(result)
    plugins, themes, mixed = resource_clues(result["final_url"], facts)
    internal = external = 0
    if facts:
        for raw in facts.links:
            link = normalize_link(result["final_url"], raw)
            if not link:
                continue
            if same_site(link, origin):
                internal += 1
            else:
                external += 1
    headers = result["headers"]
    robots_meta = facts.meta.get("robots", "") if facts else ""
    return {
        "url": display_url(result["requested_url"]),
        "final_url": display_url(result["final_url"]),
        "status": result["status"],
        "error": result["error"],
        "redirect_count": len(result["redirects"]),
        "headers_ms": result["headers_ms"],
        "total_ms": result["total_ms"],
        "content_type": headers.get("content-type"),
        "bytes_read": len(result["body"]),
        "truncated": result["truncated"],
        "title": facts.title if facts else None,
        "title_length": len(facts.title) if facts else None,
        "meta_description_present": bool(facts and facts.meta.get("description")),
        "meta_description_length": len(facts.meta.get("description", "")) if facts else None,
        "canonical": facts.canonical if facts else None,
        "lang": facts.lang if facts else None,
        "viewport_present": bool(facts and facts.meta.get("viewport")),
        "noindex": "noindex" in robots_meta.lower() or "noindex" in headers.get("x-robots-tag", "").lower(),
        "h1_count": facts.h1_count if facts else None,
        "h2_count": facts.h2_count if facts else None,
        "images": facts.images if facts else None,
        "images_without_alt_attribute": facts.images_without_alt if facts else None,
        "forms_detected_not_submitted": facts.forms if facts else None,
        "internal_links_observed": internal,
        "external_links_observed": external,
        "mixed_content_resource_count": mixed,
        "public_plugin_asset_clues": plugins,
        "public_theme_asset_clues": themes,
    }


def certificate_summary(url: str, timeout: float) -> dict[str, Any] | None:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return None
    try:
        context = ssl.create_default_context()
        with socket.create_connection((parsed.hostname, parsed.port or 443), timeout=timeout) as raw:
            with context.wrap_socket(raw, server_hostname=parsed.hostname) as secure:
                certificate = secure.getpeercert()
                expires = certificate.get("notAfter")
                expiry = datetime.fromtimestamp(ssl.cert_time_to_seconds(expires), timezone.utc) if expires else None
                return {
                    "valid": True,
                    "expires_at": expiry.isoformat() if expiry else None,
                    "days_remaining": (expiry - datetime.now(timezone.utc)).days if expiry else None,
                    "tls_version": secure.version(),
                }
    except (OSError, ssl.SSLError, ValueError) as error:
        return {"valid": False, "error": str(error)}


def wordpress_summary(home: dict[str, Any], rest: dict[str, Any]) -> dict[str, Any]:
    body = decode_body(home["body"], home["headers"].get("content-type", ""))
    facts = parse_html(home)
    score = 0
    signals: list[str] = []
    if facts and facts.generator and "wordpress" in facts.generator.lower():
        score += 2
        signals.append("WordPress generator metadata")
    if "/wp-content/" in body:
        score += 2
        signals.append("wp-content asset paths")
    if "/wp-includes/" in body:
        score += 1
        signals.append("wp-includes asset paths")
    if "api.w.org" in body:
        score += 1
        signals.append("WordPress REST discovery link")
    rest_type = rest["headers"].get("content-type", "").lower()
    rest_body = rest.get("body", b"")
    if rest.get("status") == 200 and "json" in rest_type and b'"namespaces"' in rest_body:
        score += 3
        signals.append("WordPress REST index")
    confidence = "high" if score >= 5 else "medium" if score >= 2 else "low" if score else "not detected"
    plugins, themes, _ = resource_clues(home["final_url"], facts)
    return {
        "confidence": confidence,
        "signals": signals,
        "rest_status": rest.get("status"),
        "public_plugin_asset_clues": plugins,
        "public_theme_asset_clues": themes,
        "clue_warning": "Public asset paths are not a complete active-component inventory and do not prove version, maintenance, or vulnerability status.",
    }


def audit(url: str, max_pages: int, timeout: float) -> dict[str, Any]:
    target = validate_public_url(url)
    fetcher = Fetcher(timeout)
    home = fetcher.get(target)
    if home["status"] is None:
        raise AuditError(f"Homepage request failed: {home['error']}")
    origin_parts = urlsplit(home["final_url"])
    origin = urlunsplit((origin_parts.scheme, origin_parts.netloc, "/", "", ""))

    robots_url = urljoin(origin, "robots.txt")
    robots = fetcher.get(robots_url, 200_000)
    robots_text = decode_body(robots["body"], robots["headers"].get("content-type", "")) if robots["body"] else ""
    disallowed, declared_sitemaps = robots_rules(robots_text)

    rest = fetcher.get(urljoin(origin, "wp-json/"), 250_000)
    sitemap_urls = list(dict.fromkeys(declared_sitemaps + [urljoin(origin, "wp-sitemap.xml"), urljoin(origin, "sitemap_index.xml")]))
    sitemap_results: list[dict[str, Any]] = []
    discovered: list[str] = []
    sitemap_queue = sitemap_urls[:4]
    seen_sitemaps: set[str] = set()
    while sitemap_queue and len(seen_sitemaps) < 8:
        sitemap_url = sitemap_queue.pop(0)
        if not same_site(sitemap_url, origin):
            continue
        if sitemap_url in seen_sitemaps:
            continue
        seen_sitemaps.add(sitemap_url)
        result = fetcher.get(sitemap_url, MAX_SITEMAP)
        sitemap_results.append({"url": sitemap_url, "status": result["status"], "error": result["error"]})
        if result["status"] == 200:
            text = decode_body(result["body"], result["headers"].get("content-type", ""))
            for location in sitemap_locations(text, sitemap_url):
                if urlsplit(location).path.lower().endswith(".xml"):
                    sitemap_queue.append(location)
                else:
                    discovered.append(location)

    home_facts = parse_html(home)
    if home_facts:
        for raw in home_facts.links:
            link = normalize_link(home["final_url"], raw)
            if link:
                discovered.append(link)

    candidates: list[str] = []
    for item in discovered:
        parsed = urlsplit(item)
        clean = urlunsplit((parsed.scheme, parsed.netloc, parsed.path or "/", "", ""))
        if crawlable(clean, origin, disallowed) and clean not in candidates and clean != home["final_url"]:
            candidates.append(clean)
    candidates.sort(key=page_priority)

    pages = [page_summary(home, origin)]
    for page_url in candidates[: max(0, max_pages - 1)]:
        pages.append(page_summary(fetcher.get(page_url), origin))

    headers = home["headers"]
    security_names = (
        "strict-transport-security",
        "content-security-policy",
        "x-content-type-options",
        "referrer-policy",
        "permissions-policy",
    )
    return {
        "schema": SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": display_url(target),
        "scope": {
            "mode": "bounded public read-only audit",
            "pages_requested": len(pages),
            "max_pages": max_pages,
            "forms_submitted": 0,
            "authentication_used": False,
            "external_assets_fetched": False,
            "robots_disallow_rules_respected": True,
        },
        "transport": {
            "homepage_status": home["status"],
            "final_url": display_url(home["final_url"]),
            "redirects": [display_url(item) for item in home["redirects"]],
            "https": urlsplit(home["final_url"]).scheme == "https",
            "certificate": certificate_summary(home["final_url"], timeout),
            "security_header_presence": {name: bool(headers.get(name)) for name in security_names},
            "cache_control": headers.get("cache-control"),
            "content_encoding": headers.get("content-encoding"),
        },
        "wordpress": wordpress_summary(home, rest),
        "discovery": {
            "robots": {"url": robots_url, "status": robots["status"], "error": robots["error"]},
            "robots_disallow_rule_count": len(disallowed),
            "sitemaps": sitemap_results,
            "rest": {"url": urljoin(origin, "wp-json/"), "status": rest["status"], "error": rest["error"]},
        },
        "pages": pages,
        "limitations": [
            "This is one public snapshot, not uptime history or proof that every page works.",
            "No login, WordPress admin, database, PHP log, email delivery, checkout, form submission, or destructive action was tested.",
            "Response timing is synthetic from this runner and is not field Core Web Vitals data.",
            "Use the Pressolve Connector or authorized admin/hosting evidence for plugin inventory, cron, database, and fatal-error diagnosis.",
        ],
    }


def self_test() -> None:
    sample = b'''<!doctype html><html lang="en"><head><title> Demo Site </title>
    <meta name="description" content="Demo"><meta name="viewport" content="width=device-width">
    <meta name="generator" content="WordPress 6.x"><link rel="canonical" href="https://example.com/">
    <link rel="stylesheet" href="/wp-content/themes/demo/style.css"></head>
    <body><h1>Hello</h1><img src="/image.jpg"><a href="/about/">About</a><form></form></body></html>'''
    result = {
        "requested_url": "https://example.com/",
        "final_url": "https://example.com/",
        "status": 200,
        "error": None,
        "redirects": [],
        "headers_ms": 1,
        "total_ms": 2,
        "headers": {"content-type": "text/html; charset=utf-8"},
        "body": sample,
        "truncated": False,
    }
    summary = page_summary(result, "https://example.com/")
    assert summary["title"] == "Demo Site"
    assert summary["h1_count"] == 1
    assert summary["images_without_alt_attribute"] == 1
    assert summary["forms_detected_not_submitted"] == 1
    assert summary["public_theme_asset_clues"] == ["demo"]
    assert same_site("https://www.example.com/a", "https://example.com/")
    assert not crawlable("https://example.com/about/", "https://example.com/", ["/"])
    assert not crawlable("https://example.com/checkout/", "https://example.com/", [])
    assert not crawlable("https://example.com/catalog.pdf", "https://example.com/", [])
    try:
        require_global_addresses({"127.0.0.1"})
    except AuditError:
        pass
    else:
        raise AssertionError("Private address guard failed")
    print("Pressolve Live Site Audit self-test passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", nargs="?", help="Authorized public http(s) website URL")
    parser.add_argument("--max-pages", type=int, default=8, help="Representative same-site pages, 1-20 (default: 8)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds (default: 10)")
    parser.add_argument("--output", type=Path, help="Write JSON to this path instead of stdout")
    parser.add_argument("--self-test", action="store_true", help="Run offline safety and parser tests")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if not args.url:
        parser.error("url is required unless --self-test is used")
    if not 1 <= args.max_pages <= 20:
        parser.error("--max-pages must be between 1 and 20")
    if not 1 <= args.timeout <= 30:
        parser.error("--timeout must be between 1 and 30 seconds")

    try:
        report = audit(args.url, args.max_pages, args.timeout)
    except AuditError as error:
        raise SystemExit(f"Pressolve Live Site Audit failed: {error}") from error
    output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
