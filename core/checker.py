import socket, time, asyncio, ssl

async def check_tcp(server, port, timeout=3):
    try:
        t0 = time.time()
        sock = socket.create_connection((server, port), timeout)
        sock.close()
        return True, int((time.time()-t0)*1000)
    except:
        return False, None

async def check_tls(server, port, sni=None):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((server, port), timeout=4) as sock:
            with ctx.wrap_socket(sock, server_hostname=sni or server):
                return True
    except:
        return False
