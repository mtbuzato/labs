import argparse
from pathlib import Path
import urllib.request
import ssl
import sys
import subprocess

class LabHelper:
    def __init__(self):
        super().__init__()
        self.ctx = ssl.SSLContext()

    def save(self, lab, dir, arq, subdir="/dados"):
        with urllib.request.urlopen("https://susy.ic.unicamp.br:9999/mc102w/{}-Entrega{}/{}".format(lab, subdir, arq), context=self.ctx) as res:
            with open(dir + arq, "wb") as file:
                file.write(res.read())
                file.close()
    
    def findName(self, lab):
        look = "Tarefa {}-Entrega de mc102w &mdash; ".format(lab)
        with urllib.request.urlopen("https://susy.ic.unicamp.br:9999/mc102w/{}-Entrega/".format(lab), context=self.ctx) as res:
            data = res.read().decode()
            indexStart = data.find(look)
            return data[indexStart + len(look):data.find("</H2>", indexStart)]

    def cmd_init(self, args):
        dir = "./{}/".format(args.lab)

        if(Path(dir).exists()):
            print("Já existe uma pasta chamada {}. Não pode-se prosseguir.".format(args.lab))
            return

        print("Inicializando {} com {} testes.".format(args.lab, args.tests))
        print("Carregando informações do lab...")
        name = self.findName(args.labNum)

        print("Criando arquivos...")
        Path(dir).mkdir()

        file = open(dir + "{}.py".format(args.lab), "w")
        file.write("# ------------------------------------------------------------\n# MC102W - {}: {}\n# Autor: Miguel Teixeira Buzato (185598)\n# mtbuzato.com.br\n#\n# [BREVE DESCRIÇÃO DO LAB]\n# ------------------------------------------------------------\n\nif __name__ == \"__main__\":\n    ".format(args.lab.capitalize(), name))
        file.close()

        print("Baixando enunciado...")
        self.save(args.labNum, dir, "enunc.pdf", "")

        print("Baixando testes...")
        for i in range(1, args.tests + 1):
            sys.stdout.write("\rBaixando teste {}/{}...".format(i, args.tests))
            sys.stdout.flush()
            test = "arq{:02d}".format(i)
            self.save(args.labNum, dir, test + ".in")
            self.save(args.labNum, dir, test + ".res")

        print()
        print("{} foi inicializado com sucesso.".format(args.lab))
    
    def cmd_test(self, args):
        dir = "./{}/".format(args.lab)
        if(not Path(dir).exists()):
            print("Não existe uma pasta chamada {}. Não pode-se prosseguir.".format(args.lab))
            return
        print("Testando {}...".format(args.lab))
        out = ""
        for i in range(1, args.tests + 1):
            sys.stdout.write("\rRealizando teste {}/{}...".format(i, args.tests))
            sys.stdout.flush()

            test = "arq{:02d}".format(i)

            inData = open(dir + test + ".in", "r")

            process = subprocess.run(["python", "{}.py".format(args.lab), "<{}.in".format(test)], capture_output=True, cwd=dir, input=inData.read().encode())

            if(len(process.stderr) > 0):
                print()
                print("Erro ao realizar teste {}.\n{}".format(i, process.stderr.decode("UTF-8")))
                return
            
            inData.close()

            resData = open(dir + test + ".res", "r")
            expected = resData.read()
            resData.close()

            success = expected == process.stdout.decode()

            out += "Teste {}: {}\n".format(i, "SUCESSO" if success else "FALHA")
            if not success:
                out += "Esperado:\n"
                out += expected + "\n"
                out += "Recebido:\n"
                out += process.stdout.decode()
                out += "-----------------------------\n"

        print()
        print("Testes finalizados. Relatório:")
        print(out)

helper = LabHelper()
parser = argparse.ArgumentParser(description="Utilidade para facilitar a criação e teste de labs.")
parser.add_argument("command", type=str, help="Comando da utilidade que deseja utilizar.", choices=[cmd[4:] for cmd in dir(helper) if cmd.startswith("cmd_")])
parser.add_argument("lab", type=int, help="Número do lab que deseja trabalhar com.")
parser.add_argument("-t", "--tests", type=int, help="Número de testes que o lab possui.", default=15)

args = parser.parse_args()
args.labNum = "{:02d}".format(args.lab)
args.lab = "lab" + args.labNum
getattr(helper, "cmd_" + args.command)(args)