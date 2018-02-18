import os
import subprocess
import random
class Mutate:
    def __init__(self, corpus='./corpus', fextention='pdf'):
        self.files = os.listdir(corpus)
        self.corpus_dir = corpus
        self.extention = fextention
    def _pick_file(self):
        return random.choice(self.files)
    def mutate(self, filename, upper_limit=1024, lower_limit=128):
        f = open(filename,'r').read()
        file_size = os.stat(filename).st_size
        bytes_to_change = random.randint(lower_limit, upper_limit)
        new_bytes = os.urandom(bytes_to_change)
        for i in range(0, bytes_to_change):
            byte_to_change = random.randint(50, file_size)
            f = f[:byte_to_change-1]+new_bytes[i]+f[byte_to_change+1:]
        a = open('/tmp/a.{}'.format(self.extention), 'w')
        a.write(f)
        a.close()
        return '/tmp/a.{}'.format(self.extention)
    def trigger(self, command, file):
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.check_call([command, file, '/tmp/a.txt'], stdout=devnull,
                                      stderr=devnull, shell=True)
        except subprocess.CalledProcessError as e:
            if e.returncode == 139:
                print("SEGFAULT")
                exit(-1)
    def next(self):
        file_to_mutate = "{}/{}".format(self.corpus_dir, self._pick_file())
        new_file = self.mutate(file_to_mutate)
        self.trigger('pdftotext', new_file)

if __name__ == "__main__":
    a = Mutate()
    while True:
        a.next()
