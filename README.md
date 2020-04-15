# Laboratórios de MC102 da Unicamp (Turma W)

Este repositório contém os enunciados, arquivos de testes e solução(própria) dos Laboratórios de MC102W da Unicamp, e uma ferramenta para facilitar o desenvolvimento e teste de novos laboratórios.

## Como utilizar a ferramenta

`python lab.py [-h] [-t TESTS] {init,test} lab`

### Comandos

#### init

Cria uma nova pasta para o lab e faz o download do enunciado, arquivos de teste e cria o arquivo para ser editado.

#### test

Roda os testes do lab especificado.

### Argumentos

#### lab

Número do lab que deseja trabalhar com.

### Argumentos Opcionais

#### -h, --help

Exibe a mensagem de ajuda.

#### -t TESTS --tests TESTS

Define um número de testes para o lab. *Padrão: 15*