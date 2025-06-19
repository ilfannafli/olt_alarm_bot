import time
def wait_for_output(shell, olt, command, expected_string, timeout=10):
        shell.send(command)
        buffer = ""
        start_time = time.time()

        while True:
            if shell.recv_ready():
                output = shell.recv(1024).decode('utf-8')
                buffer += output
                #print("[DEBUG OUTPUT]:", repr(output))  # <=== tambahin ini buat cek apa yg dikirim balik
                #print("CEK :",command)
                #print("hasil :",buffer)
                if expected_string in buffer:
                    #print("[MATCH]:", expected_string)
                    #print("[FULL BUFFER]:", buffer)
                    #print("berhasil :",command)
                    return buffer
            if time.time() - start_time > timeout:
                print("Timeout untuk olt : ",olt)
                return None
            time.sleep(0.2)