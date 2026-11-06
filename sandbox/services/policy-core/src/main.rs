// Policy Core — Rust/Axum
// Authorization, evidence controls (CIA, SOC 2, ISO 27001, NIST)
// Runs as UID 1001 in a minimal Alpine container.

use axum::{routing::get, Router};
use std::env;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    // Validate required env vars at startup
    for var in &["DATABASE_URL", "JWT_ISSUER"] {
        if env::var(var).is_err() {
            eprintln!("FATAL: Required env var '{}' is not set", var);
            std::process::exit(1);
        }
    }

    let port: u16 = env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse()
        .unwrap_or(8080);

    let app = Router::new()
        .route("/health", get(health))
        .route("/ready", get(ready))
        .route("/policy/evaluate", get(evaluate));

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    tracing::info!("Policy core listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn health() -> impl axum::response::IntoResponse {
    serde_json::json!({
        "status": "healthy",
        "service": "policy-core",
        "uid": unsafe { libc::getuid() }
    })
}

async fn ready() -> impl axum::response::IntoResponse {
    serde_json::json!({"status": "ready"})
}

async fn evaluate() -> impl axum::response::IntoResponse {
    serde_json::json!({
        "decision": "allow",
        "controls": ["CIA", "SOC2-CC6", "ISO27001-A9", "NIST-AC2"]
    })
}
