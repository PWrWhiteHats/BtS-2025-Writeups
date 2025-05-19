use aes::cipher::{BlockDecryptMut, KeyIvInit, block_padding::Pkcs7};
use base64::prelude::*;
use serde::{Deserialize, Serialize};
use std::error::Error;
type Aes256CbcDec = cbc::Decryptor<aes::Aes256>;

#[derive(Serialize, Debug)]
struct Request {
    amount: u32,
}

#[derive(Deserialize, Debug)]
struct Response {
    flags: Vec<(String, u128)>,
}

fn decrypt_flag(key: &[u8], iv: &[u8], ciphertext: &[u8]) -> Result<Vec<u8>, Box<dyn Error>> {
    let mut ct = BASE64_STANDARD
        .decode(ciphertext)
        .map_err(|_| "Base64 decoding failed")?;
    let cipher = Aes256CbcDec::new_from_slices(key, iv).unwrap();
    let ct = cipher
        .decrypt_padded_mut::<Pkcs7>(&mut ct)
        .map_err(|_| "Decryption failed")?;
    Ok(ct.to_vec())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    // Create the request payload
    let request = Request { amount: 64 };

    // Create a client and send the POST request
    let client = reqwest::Client::new();

    // Check if the request was successful
    'outer: loop {
        let response = client
            .get("http://localhost:1337/flags")
            .json(&request)
            .send()
            .await?;

        if response.status().is_success() {
            // Parse the JSON response
            let data: Response = response.json().await?;
            for (flag, iv) in data.flags {
                if let Ok(decrypted) = decrypt_flag(&[0; 32], &iv.to_le_bytes(), &flag.as_bytes()) {
                    if let Ok(decrypted) = String::from_utf8(decrypted) {
                        println!("Decrypted flag: {}", decrypted);
                        break 'outer;
                    }
                }
            }
        } else {
            println!("Request failed with status: {}", response.status());
        }
    }

    Ok(())
}
