# ------------------------------------------------------------
# MC102W - Lab07: Guerra 4.0
# Autor: Miguel Teixeira Buzato (185598)
# mtbuzato.com.br
#
# Programa de computador que serve para descobrir, através de
# etapas em um duelo, qual herói ganha na Guerra
# ------------------------------------------------------------

# ATENÇÃO: devido ao tamanho deste arquivo, o SuSy não permitiu que eu fizesse o upload do arquivo com comentários.
# Portanto, esta versão está minificada e é ilegível.
# Para ver a versão com comentários e espacamento, acesse: https://gist.github.com/mtbuzato/ff2e687f3cb3441cbc7edc96c510d462
# Qualquer problema por favor entrar em contato comigo:
#   m185598@dac.unicamp.br
#   miguel@mtbuzato.com.br
# Para ter certeza de que não alterei nada após a data, deixo aqui marcada a data de envio: 04/05/2020
# Para confirmar que não houveram alterações, a aba Revisões do Gist serve de prova

class Hero:
	def __init__(self,name,hp,dmg,armor,mana):self.name=name;self.maxHp=hp;self.hp=hp;self.dmg=dmg;self.initialDmg=dmg;self.armor=armor;self.maxMana=mana;self.mana=mana;self.cards={};self.insaneAttacks=0;self.insaneDmg=0;self.invincibility=0;self.drain=0
	def use(self,card,target):
		if card.used:print(f"{self.name} já ativou a carta {card.name}")
		elif card.instant or card.representation in self.cards:
			if self.mana<card.cost:print(f"{self.name} não possui mana suficiente para a mágica")
			else:
				if not card.instant and not card.passive:print(f"{self.name} ativou a carta {card.name}")
				self.mana=max(0,self.mana-card.cost);card.used=True;card.use(self,target)
		else:print(f"{self.name} não possui a carta {card.name}")
	def attack(self,target):
		if self.insaneAttacks>0:print(f"{self.name} deu um ataque insano em {target.name}");self.insaneAttacks-=1
		else:print(f"{self.name} atacou {target.name}")
		if target.invincibility>0:
			print(f"{target.name} estava invulnerável");target.invincibility-=1
			if target.invincibility==0:del target.cards['S']
		else:dmg=self.dmg+self.insaneDmg;target.hp=max(0,target.hp-(dmg-int(dmg*target.armor/100)))
		if self.drain>0:target.mana=max(0,target.mana-self.drain)
		if self.insaneAttacks==0 and self.insaneDmg>0:self.insaneDmg=0;del self.cards['I']
class CardDefinition:
	def __init__(self,name,createFunction,representation=None,instant=False,passive=False):self.name=name;self.representation=representation if representation!=None else name[0];self.instant=instant;self.passive=passive;self.createFunction=createFunction
	def create(self,cmdList):return self.createFunction(self,cmdList)
class Card:
	def __init__(self,definition,cost=0):self.name=definition.name;self.representation=definition.representation;self.instant=definition.instant;self.passive=definition.passive;self.cost=cost;self.used=False
	def use(self,hero,target):raise NotImplementedError('Esta carta não possui função atribuída.')
class HealCard(Card):
	def __init__(self,definition,cost,healing):super().__init__(definition,cost=cost);self.healing=healing
	def use(self,hero,target):hero.hp=min(hero.maxHp,hero.hp+self.healing)
class ForceCard(Card):
	def __init__(self,definition,cost,force):super().__init__(definition,cost=cost);self.force=force
	def use(self,hero,target):hero.dmg+=self.force
class ProtectionCard(Card):
	def __init__(self,definition,cost,protection):super().__init__(definition,cost=cost);self.protection=protection
	def use(self,hero,target):hero.armor=min(100,hero.armor+self.protection)
class EterCard(Card):
	def __init__(self,definition,manaPoints):super().__init__(definition);self.manaPoints=manaPoints
	def use(self,hero,target):hero.mana=min(hero.maxMana,hero.mana+self.manaPoints)
class DrainCard(Card):
	def __init__(self,definition,drainPoints):super().__init__(definition);self.drainPoints=drainPoints
	def use(self,hero,target):hero.drain=self.drainPoints
class InsaneCard(Card):
	def __init__(self,definition,cost,insaneAttacks,dmgBoost):super().__init__(definition,cost=cost);self.insaneAttacks=insaneAttacks;self.dmgBoost=dmgBoost
	def use(self,hero,target):hero.insaneAttacks=self.insaneAttacks;hero.insaneDmg=self.dmgBoost
class StarCard(Card):
	def __init__(self,definition,cost,invincibility):super().__init__(definition,cost=cost);self.invincibility=invincibility
	def use(self,hero,target):hero.invincibility=self.invincibility
cards={}
def createHero():return Hero(str(input()),int(input()),int(input()),int(input()),int(input()))
def registerCard(definition):cards[definition.representation]=definition
def printStatus(heros):
	for hero in heros:print(f"{hero.name} possui {hero.hp} de vida, {hero.mana} pontos mágicos, {hero.dmg} de dano e {hero.armor}% de bloqueio")
if __name__=='__main__':
	registerCard(CardDefinition('Cura',lambda definition,cmdList:HealCard(definition,int(cmdList[0]),int(cmdList[1])),instant=True));registerCard(CardDefinition('Força',lambda definition,cmdList:ForceCard(definition,int(cmdList[0]),int(cmdList[1])),instant=True));registerCard(CardDefinition('Proteção',lambda definition,cmdList:ProtectionCard(definition,int(cmdList[0]),int(cmdList[1])),instant=True));registerCard(CardDefinition('Éter',lambda definition,cmdList:EterCard(definition,int(cmdList[0])),instant=True,representation='E'));registerCard(CardDefinition('Drenagem',lambda definition,cmdList:DrainCard(definition,int(cmdList[0])),passive=True));registerCard(CardDefinition('Insano',lambda definition,cmdList:InsaneCard(definition,int(cmdList[0]),int(cmdList[1]),int(cmdList[2]))));registerCard(CardDefinition('Estrela',lambda definition,cmdList:StarCard(definition,int(cmdList[0]),int(cmdList[1])),representation='S'));snow=createHero();sunny=createHero();print(f"O reino Snowland indicou o herói {snow.name}");print(f"O reino Sunny Kingdom indicou o herói {sunny.name}");attacking=None;defending=None;turn=1;turnActions=0;fighting=True
	while fighting:
		try:cmdList=str(input()).split(' ')
		except EOFError:fighting=False
		except:print('Erro desconhecido.')
		else:
			cmd=cmdList.pop(0)
			if cmd=='H':
				if int(cmdList[0])==1:attacking=snow;defending=sunny
				else:attacking=sunny;defending=snow
				turnActions+=1;print(f"Rodada {turn}: vez de {attacking.name}")
			elif cmd=='M':
				cardFoundRepresentation=str(cmdList.pop(0))
				if cardFoundRepresentation=='X':print(f"{attacking.name} não encontrou nenhuma carta")
				elif not cardFoundRepresentation in cards:raise ValueError('Carta inválida encontrada.')
				else:
					cardFound=cards[cardFoundRepresentation].create(cmdList);print(f"{attacking.name} encontrou a carta {cardFound.name}")
					if cardFound.instant:attacking.use(cardFound,defending)
					elif cardFound.representation in attacking.cards:print(f"{attacking.name} já possui a carta {cardFound.name}")
					else:
						attacking.cards[cardFound.representation]=cardFound
						if cardFound.passive:attacking.use(cardFound,defending)
			elif cmd=='A':
				attacking.attack(defending)
				if turnActions>1:turnActions=0;turn+=1;printStatus([snow,sunny])
				if snow.hp==0 or sunny.hp==0:fighting=False
			elif len(cmd)!=0:
				if not cmd in cards:raise ValueError('Tentou utilizar uma cartá inexistente.')
				elif not cmd in attacking.cards:print(f"{attacking.name} não possui a carta {cards[cmd].name}")
				else:attacking.use(attacking.cards[cmd],defending)
	if snow.hp<=0:print(f"O herói {sunny.name} do reino Sunny Kingdom venceu o duelo")
	else:print(f"O herói {snow.name} do reino Snowland venceu o duelo")
	printStatus([snow,sunny])