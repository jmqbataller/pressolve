<?php
/**
 * Plugin Name: Pressolve Connector
 * Plugin URI: https://github.com/jmqbataller/pressolve
 * Description: Generates an administrator-reviewed, sanitized diagnostic report for Pressolve without remote access or stored exports.
 * Version: 2.0.0
 * Author: John Mark Bataller
 * Author URI: https://jmqbataller.vercel.app/
 * License: MIT
 * Requires at least: 6.5
 * Requires PHP: 7.4
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

final class Pressolve_Connector {
	const VERSION = '2.0.0';

	/** Register administrator-only hooks. */
	public static function init() {
		add_action( 'admin_menu', array( __CLASS__, 'register_page' ) );
		add_action( 'admin_post_pressolve_download_report', array( __CLASS__, 'download_report' ) );
	}

	/** Add Tools > Pressolve Report. */
	public static function register_page() {
		add_management_page(
			__( 'Pressolve Report', 'pressolve-connector' ),
			__( 'Pressolve Report', 'pressolve-connector' ),
			'manage_options',
			'pressolve-report',
			array( __CLASS__, 'render_page' )
		);
	}

	/** Render a reviewable report without persisting it. */
	public static function render_page() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( esc_html__( 'You do not have permission to view this report.', 'pressolve-connector' ) );
		}

		$report = self::collect_report();
		$json   = wp_json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );
		?>
		<div class="wrap">
			<h1><?php echo esc_html__( 'Pressolve Diagnostic Report', 'pressolve-connector' ); ?></h1>
			<p><?php echo esc_html__( 'Review this sanitized, read-only snapshot before downloading or sharing it. No report is stored or transmitted by this plugin.', 'pressolve-connector' ); ?></p>
			<p><strong><?php echo esc_html__( 'Important:', 'pressolve-connector' ); ?></strong> <?php echo esc_html__( 'Automatic redaction cannot guarantee that every sensitive value is detected.', 'pressolve-connector' ); ?></p>
			<textarea readonly class="large-text code" rows="28" aria-label="<?php echo esc_attr__( 'Pressolve diagnostic JSON preview', 'pressolve-connector' ); ?>"><?php echo esc_textarea( $json ); ?></textarea>
			<form action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" method="post">
				<input type="hidden" name="action" value="pressolve_download_report">
				<?php wp_nonce_field( 'pressolve_download_report' ); ?>
				<?php submit_button( __( 'Download pressolve-report.json', 'pressolve-connector' ) ); ?>
			</form>
		</div>
		<?php
	}

	/** Send a freshly generated report directly to the administrator. */
	public static function download_report() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( esc_html__( 'You do not have permission to download this report.', 'pressolve-connector' ) );
		}
		check_admin_referer( 'pressolve_download_report' );

		$report = self::collect_report();
		$json   = wp_json_encode( $report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES );

		nocache_headers();
		header( 'Content-Type: application/json; charset=utf-8' );
		header( 'Content-Disposition: attachment; filename="pressolve-report.json"' );
		header( 'X-Content-Type-Options: nosniff' );
		echo $json; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped -- JSON download, already encoded.
		exit;
	}

	/** Collect a minimal, read-only, sanitized diagnostic snapshot. */
	private static function collect_report() {
		global $wpdb, $wp_version;

		if ( ! function_exists( 'get_plugins' ) ) {
			require_once ABSPATH . 'wp-admin/includes/plugin.php';
		}

		$active_plugins  = (array) get_option( 'active_plugins', array() );
		$network_plugins = is_multisite() ? (array) get_site_option( 'active_sitewide_plugins', array() ) : array();
		$plugin_files    = array_values( array_unique( array_merge( $active_plugins, array_keys( $network_plugins ) ) ) );
		$plugins         = get_plugins();
		$plugin_items    = array();

		foreach ( $plugin_files as $plugin_file ) {
			$data           = isset( $plugins[ $plugin_file ] ) ? $plugins[ $plugin_file ] : array();
			$directory      = dirname( $plugin_file );
			$plugin_items[] = array(
				'slug'           => '.' === $directory ? sanitize_key( basename( $plugin_file, '.php' ) ) : sanitize_key( $directory ),
				'name'           => isset( $data['Name'] ) ? wp_strip_all_tags( $data['Name'] ) : 'Unknown plugin',
				'version'        => isset( $data['Version'] ) ? sanitize_text_field( $data['Version'] ) : 'unknown',
				'network_active' => isset( $network_plugins[ $plugin_file ] ),
			);
		}

		usort(
			$plugin_items,
			static function ( $left, $right ) {
				return strcasecmp( $left['name'], $right['name'] );
			}
		);

		$theme        = wp_get_theme();
		$parent_theme = $theme->parent();
		$cron         = self::cron_summary();
		$rest         = self::rest_check();
		$database     = self::database_summary( $wpdb );

		$report = array(
			'schema'            => 'pressolve-report/v1',
			'generated_at'      => gmdate( 'c' ),
			'connector_version' => self::VERSION,
			'environment'       => array(
				'type'            => function_exists( 'wp_get_environment_type' ) ? wp_get_environment_type() : 'unknown',
				'wordpress'       => $wp_version,
				'php'             => PHP_VERSION,
				'database'        => method_exists( $wpdb, 'db_version' ) ? $wpdb->db_version() : 'unknown',
				'server'          => isset( $_SERVER['SERVER_SOFTWARE'] ) ? sanitize_text_field( wp_unslash( $_SERVER['SERVER_SOFTWARE'] ) ) : 'unknown',
				'multisite'       => is_multisite(),
				'locale'          => get_locale(),
				'memory_limit'    => defined( 'WP_MEMORY_LIMIT' ) ? WP_MEMORY_LIMIT : ini_get( 'memory_limit' ),
				'max_upload_size' => wp_max_upload_size(),
			),
			'site'              => array(
				'https'                 => is_ssl(),
				'debug'                 => defined( 'WP_DEBUG' ) && WP_DEBUG,
				'debug_display'         => defined( 'WP_DEBUG_DISPLAY' ) && WP_DEBUG_DISPLAY,
				'permalink_configured'  => '' !== (string) get_option( 'permalink_structure' ),
				'search_engine_visible' => '1' === (string) get_option( 'blog_public', '1' ),
			),
			'theme'             => array(
				'name'           => $theme->get( 'Name' ),
				'version'        => $theme->get( 'Version' ),
				'parent_name'    => $parent_theme ? $parent_theme->get( 'Name' ) : null,
				'parent_version' => $parent_theme ? $parent_theme->get( 'Version' ) : null,
				'block_theme'    => function_exists( 'wp_is_block_theme' ) ? wp_is_block_theme() : null,
			),
			'plugins'           => array(
				'active_count'         => count( $plugin_items ),
				'network_active_count' => count( $network_plugins ),
				'items'                => $plugin_items,
			),
			'cache'             => array(
				'wp_cache'               => defined( 'WP_CACHE' ) && WP_CACHE,
				'object_cache_dropin'    => file_exists( WP_CONTENT_DIR . '/object-cache.php' ),
				'advanced_cache_dropin'  => file_exists( WP_CONTENT_DIR . '/advanced-cache.php' ),
			),
			'cron'              => $cron,
			'database'          => $database,
			'rest'              => $rest,
			'woocommerce'       => self::woocommerce_summary(),
			'recent_fatals'     => self::recent_fatals(),
		);

		return self::redact_recursive( $report );
	}

	/** Summarize cron without exposing hooks or arguments. */
	private static function cron_summary() {
		$crons   = function_exists( '_get_cron_array' ) ? _get_cron_array() : array();
		$total   = 0;
		$overdue = 0;
		$next    = null;
		$now     = time();

		foreach ( (array) $crons as $timestamp => $hooks ) {
			foreach ( (array) $hooks as $instances ) {
				$count    = count( (array) $instances );
				$total   += $count;
				$overdue += ( (int) $timestamp < $now - 300 ) ? $count : 0;
			}
			if ( null === $next || (int) $timestamp < $next ) {
				$next = (int) $timestamp;
			}
		}

		return array(
			'total_events'   => $total,
			'overdue_events' => $overdue,
			'next_event_utc' => $next ? gmdate( 'c', $next ) : null,
		);
	}

	/** Perform one short, same-site public REST check. */
	private static function rest_check() {
		$response = wp_remote_get(
			rest_url(),
			array(
				'timeout'             => 4,
				'redirection'         => 1,
				'limit_response_size' => 4096,
				'user-agent'          => 'Pressolve-Connector/' . self::VERSION,
			)
		);

		if ( is_wp_error( $response ) ) {
			return array(
				'status'     => null,
				'error_code' => sanitize_key( $response->get_error_code() ),
			);
		}

		return array(
			'status'     => (int) wp_remote_retrieve_response_code( $response ),
			'error_code' => null,
		);
	}

	/** Collect size totals without reading option values into the report. */
	private static function database_summary( $wpdb ) {
		$database_size = $wpdb->get_var( 'SELECT SUM(data_length + index_length) FROM information_schema.tables WHERE table_schema = DATABASE()' ); // phpcs:ignore WordPress.DB.DirectDatabaseQuery.DirectQuery
		$autoload_size = $wpdb->get_var( "SELECT SUM(LENGTH(option_value)) FROM {$wpdb->options} WHERE autoload IN ('yes','on','auto','auto-on')" ); // phpcs:ignore WordPress.DB.DirectDatabaseQuery.DirectQuery,WordPress.DB.PreparedSQL.InterpolatedNotPrepared

		return array(
			'size_bytes'     => is_numeric( $database_size ) ? (int) $database_size : null,
			'autoload_bytes' => is_numeric( $autoload_size ) ? (int) $autoload_size : null,
		);
	}

	/** Return non-sensitive WooCommerce compatibility indicators. */
	private static function woocommerce_summary() {
		$active = defined( 'WC_VERSION' );
		$hpos   = null;

		if ( $active && class_exists( '\\Automattic\\WooCommerce\\Utilities\\OrderUtil' ) ) {
			$hpos = \Automattic\WooCommerce\Utilities\OrderUtil::custom_orders_table_usage_is_enabled();
		}

		return array(
			'active'  => $active,
			'version' => $active ? WC_VERSION : null,
			'hpos'    => $hpos,
		);
	}

	/** Read only a small tail of fatal-error lines and redact it. */
	private static function recent_fatals() {
		$path = WP_CONTENT_DIR . '/debug.log';
		if ( ! is_readable( $path ) || ! is_file( $path ) ) {
			return array();
		}

		$size = filesize( $path );
		if ( false === $size ) {
			return array();
		}

		$offset   = $size > 65536 ? $size - 65536 : 0;
		$contents = file_get_contents( $path, false, null, $offset, 65536 ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
		if ( false === $contents ) {
			return array();
		}

		$lines  = preg_split( '/\R/', $contents );
		$fatals = array();
		foreach ( (array) $lines as $line ) {
			if ( preg_match( '/(?:PHP Fatal error|Uncaught (?:Error|Exception)|PHP Parse error)/i', $line ) ) {
				$fatals[] = self::redact_text( $line );
			}
		}

		return array_slice( $fatals, -20 );
	}

	/** Redact strings recursively as a final defense before display/download. */
	private static function redact_recursive( $value ) {
		if ( is_array( $value ) ) {
			foreach ( $value as $key => $item ) {
				$value[ $key ] = self::redact_recursive( $item );
			}
			return $value;
		}
		return is_string( $value ) ? self::redact_text( $value ) : $value;
	}

	/** Redact common personal, location, and credential-like patterns. */
	private static function redact_text( $text ) {
		$text = wp_normalize_path( $text );
		$text = str_replace( wp_normalize_path( WP_CONTENT_DIR ), '[CONTENT]', $text );
		$text = str_replace( wp_normalize_path( ABSPATH ), '[ABSPATH]/', $text );
		$text = preg_replace( '/\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i', '[EMAIL]', $text );
		$text = preg_replace( '/\b(?:\d{1,3}\.){3}\d{1,3}\b/', '[IP]', $text );
		$text = preg_replace( '#https?://[^\s\'"<>]+#i', '[URL]', $text );
		$text = preg_replace( '/\b[A-Z]:\/[^\s]+/i', '[WINDOWS_PATH]', $text );
		$text = preg_replace( '#(?<![A-Za-z0-9])/(?:[^/\s]+/)+[^/\s:]+#', '[PATH]', $text );
		$text = preg_replace( '/\b(?:Bearer|Basic)\s+[A-Za-z0-9._~+\/=:-]+/i', '[AUTHORIZATION]', $text );
		$text = preg_replace( '/\b(?:api[_-]?key|secret|token|password|license[_-]?key)\b\s*[:=]\s*[^\s,;]+/i', '[REDACTED_SECRET]', $text );
		return sanitize_text_field( $text );
	}
}

Pressolve_Connector::init();
