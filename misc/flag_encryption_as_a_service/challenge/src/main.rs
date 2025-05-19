#![feature(vec_into_raw_parts)]
use aes::cipher::{BlockEncryptMut, KeyIvInit, block_padding::Pkcs7};
use axum::{Router, extract::Json, http::StatusCode, routing::get};
use base64::prelude::*;
use std::arch::x86_64;
type Aes256CbcEnc = cbc::Encryptor<aes::Aes256>;

lazy_static::lazy_static! {
    static ref FLAG: String = format!("BtSCTF{{0h_n0_s0m5_k5ys_ar3_un1n1tl1z3d-{}}}", std::env::var("FLAG").unwrap_or_else(|_| {
        println!("THE FLAG ENVIRONMENT VARIABLE HAS NOT BEEN SET!!!");
        std::process::exit(1);
    }));
}

fn encrypt_flag(key: [u8; 32], iv: [u8; 16], flag: &str) -> String {
    let mut flag_bytes = flag.as_bytes().to_vec();
    let len = flag_bytes.len();
    flag_bytes.extend_from_slice([0u8; 16].as_ref());
    let ct = Aes256CbcEnc::new(&key.into(), &iv.into())
        .encrypt_padded_mut::<Pkcs7>(&mut flag_bytes, len)
        .unwrap_or_else(|e| panic!("Encryption failed: {e:?}"));
    BASE64_STANDARD.encode(ct)
}

fn make_keys(count: usize) -> Vec<[u8; 32]> {
    let mut keys: Vec<u64> = vec![0; count * 4];
    for num in keys.iter_mut() {
        unsafe { x86_64::_rdseed64_step(num) };
    }
    unsafe {
        let (ptr, length, capacity) = keys.into_raw_parts();
        Vec::from_raw_parts(ptr as *mut [u8; 32], length / 4, capacity / 4)
    }
}

fn make_iv() -> [u8; 16] {
    let mut iv = [0u64; 2];
    for i in iv.iter_mut() {
        unsafe { x86_64::_rdseed64_step(i) };
    }
    unsafe { std::mem::transmute(iv) }
}

// Define request and response structs
#[derive(serde::Deserialize)]
struct FlagRequest {
    amount: usize,
}

#[derive(serde::Serialize)]
struct FlagResponse {
    flags: Vec<(String, u128)>,
}

async fn get_encrypted_flags(
    Json(request): Json<FlagRequest>,
) -> Result<Json<FlagResponse>, StatusCode> {
    // Validate the request
    if request.amount > 64 || request.amount == 0 {
        return Err(StatusCode::BAD_REQUEST);
    }

    let amount = request.amount;
    let mut encrypted_flags = Vec::with_capacity(amount);

    // Generate keys and IVs
    #[allow(non_snake_case)]
    let mut iv = u128::from_ne_bytes(make_iv());
    let keys = make_keys(amount);
    // Encrypt the flags
    for key in keys {
        iv += 1;
        let encrypted = encrypt_flag(key, iv.to_ne_bytes(), &FLAG);
        encrypted_flags.push((encrypted, iv));
    }

    // Return the encrypted flags
    Ok(Json(FlagResponse {
        flags: encrypted_flags,
    }))
}

#[tokio::main]
async fn main() {
    // Set up the Axum router with /flags endpoint
    let app = Router::new().route("/flags", get(get_encrypted_flags));

    // Start the server on port 1337
    let listener = tokio::net::TcpListener::bind("0.0.0.0:1337").await.unwrap();
    axum::serve(listener, app)
        .await
        .expect("Axum server failed!");
}
