class Buffer:
    def load_buffer(self, path):
        print(path)
        arq = open(path, "r")
        text = arq.readline()

        buffer = []
        cont = 1

        # The buffer size can be changed by changing cont
        while text != "":
            buffer.append(text)
            text = arq.readline()
            cont += 1

            if cont == 10 or text == "":
                # Return a full buffer
                buf = "".join(buffer)
                cont = 1
                yield buf

                # Reset the buffer
                buffer = []

        # reset the file pointer to get all content of file. will be used to display content of file in UI
        arq.seek(0)
        whole_file = arq.read()
        arq.close()

        return whole_file
