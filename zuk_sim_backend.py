from random import randint
import time

class NPC:
	def __init__(self, hp):
		self.hp = self.base_hp = hp

	def heal_hp(self, amount):
		self.hp += amount
		if self.hp > self.base_hp:
			self.hp = self.base_hp #Don't heal above max hp

	def lower_hp(self, damage):
		self.hp -= damage
		if self.hp < 0:
			self.hp = 0 #Don't put hp into negatives

def simHit(accuracy, maxHit):
	accuracy_rand = randint(0, 10000) #Working with numbers above 0 to avoid the chance of floating point errors affecting the results
	hit = randint(0, maxHit)
	if accuracy * 10000 >= accuracy_rand:
		return hit
	else:
		return 0

def healZuk(NPC):
	heal_amount = randint(15,24)
	NPC.heal_hp(heal_amount)

def healJad(NPC, triples = False, zukJad = False):
	heal_amount = 0
	if triples or zukJad:
		for i in range(2):
			heal_amount += randint(15, 24)
	else:
		for i in range(3):
			heal_amount += randint(15,24)
	NPC.heal_hp(heal_amount)


def getDamage(gear, npc, weapon):
	if gear in ['Task Standard', 'Task Archers', "Task Devout"]:
		if weapon == "Twisted bow":
			max_hit = 83
		elif weapon == "Toxic blowpipe":
			max_hit = 34
	elif gear in ['Off Task Standard', 'Off Task Devout']:
		if weapon == "Twisted bow":
			max_hit = 73
		elif weapon == "Toxic blowpipe":
			max_hit = 30
	if npc == "Zuk" and weapon == "Twisted bow":
		if gear == "Task Standard":
			accuracy = 0.5929
		elif gear == "Task Archers":
			accuracy = 0.6062
		elif gear == "Task Devout":
			accuracy = 0.5712
		elif gear == "Off Task Standard":
			accuracy = 0.5453
		elif gear == "Off Task Devout":
			accuracy = 0.5217
	elif npc == "Ranger" and weapon == "Toxic blowpipe":
		if gear == "Task Standard":
			accuracy = 0.9448
		elif gear == "Task Archers":
			accuracy = 0.9465
		elif gear == "Task Devout":
			accuracy = 0.9419
		elif gear == "Off Task Standard":
			accuracy = 0.9393
		elif gear == "Off Task Devout":
			accuracy = 0.9352
	elif npc == "Mager" and weapon == "Twisted bow":
		if gear == "Task Standard":
			accuracy = 0.8411
		elif gear == "Task Archers":
			accuracy = 0.8463
		elif gear == "Task Devout":
			accuracy = 0.8326
		elif gear == "Off Task Standard":
			accuracy = 0.8225
		elif gear == "Off Task Devout":
			accuracy = 0.8133
	elif npc == "Mager" and weapon == "Toxic blowpipe":
		if gear == "Task Standard":
			accuracy = 0.7848
		elif gear == "Task Archers":
			accuracy = 0.7916
		elif gear == "Task Devout":
			accuracy = 0.7737
		elif gear == "Off Task Standard":
			accuracy = 0.7594
		elif gear == "Off Task Devout":
			accuracy = 0.7474
	elif npc == "Jad" and weapon == "Twisted bow":
		if gear == "Task Standard":
			accuracy = 0.7112
		elif gear == "Task Archers":
			accuracy = 0.7206
		elif gear == "Task Devout":
			accuracy = 0.6958
		elif gear == "Off Task Standard":
			accuracy = 0.6774
		elif gear == "Off Task Devout":
			accuracy = 0.6607
	elif npc == "Healer":
		if gear == "Task Standard":
			accuracy = 0.9128
		elif gear == "Task Archers":
			accuracy = 0.9156
		elif gear == "Task Devout":
			accuracy = 0.9083
		elif gear == "Off Task Standard":
			accuracy = 0.9025
		elif gear == "Off Task Devout":
			accuracy = 0.8976
	return max_hit, accuracy

def killZuk(gear = "Task Standard", doKillMager = False, doKillJad = False, doKillHealers = False):
	bow_max_hit, bow_accuracy = getDamage(gear, "Zuk", "Twisted bow")
	zuk = NPC(1200)
	bow_hits = 0
	bp_hits = 0
	spec_regen_bow_hits = 0
	spec_regen_bp_hits = 0
	countSpec = False
	zukHealed = False
	jadSpawned = False
	spawnSets = False
	wasSet = True
	healer_specs = 0
	while zuk.hp > 0: 
		bow_damage = simHit(bow_accuracy, bow_max_hit)
		zuk.lower_hp(bow_damage)
		bow_hits += 1
		if countSpec:
			spec_regen_bow_hits += 1
		if bow_hits == 14:
			if zuk.hp < 600:
				spawnSets = False
				wasSet = False
			else:
				spawnSets = True
		if spawnSets:
			bp_hits += killRanger(2, gear)
			if spec_regen_bp_hits == 0:
				spec_regen_bp_hits = bp_hits - 2
				countSpec = True
			if doKillMager:
				bow_hits_to_kill_mager = killMager(gear, False)[0]
				bow_hits += bow_hits_to_kill_mager
				if countSpec:
					spec_regen_bow_hits += bow_hits_to_kill_mager
			spawnSets = False
		if zuk.hp < 480 and not jadSpawned and doKillJad:
			bow_hits += killJad(gear, False, True)
			if countSpec:
				spec_regen_bow_hits += 1
			jadSpawned = True
		if zuk.hp < 240 and not zukHealed:
			for i in range(7):
				healZuk(zuk)
			zukHealed = True
			total_spec_regen_ticks = getCombatTime(spec_regen_bow_hits, spec_regen_bp_hits)
			while total_spec_regen_ticks > 250 and healer_specs < 2:
				healer_specs += 1
				total_spec_regen_ticks -= 250
			if doKillHealers:
				for i in range(4):
					if healer_specs > 1:
						bp_hits += killHealer(1, gear)
						healer_specs -= 1
					else:
						bp_hits += killHealer(0, gear)
	return bow_hits, bp_hits, wasSet

def killJad(gear = "Task Standard", triples = False, isZukJad = False):
	bow_max_hit, bow_accuracy = getDamage(gear, "Zuk", "Twisted bow")
	jad = NPC(350)
	bow_hits = 0
	jadHealed = False
	while jad.hp > 0:
		bow_damage = simHit(bow_accuracy, bow_max_hit)
		bow_hits += 1
		jad.lower_hp(bow_damage)
		if jad.hp < 175 and not jadHealed:
			healJad(jad, triples, isZukJad)
			jadHealed = True
	return bow_hits

def killTripleJads(gear = "Task Standard"):
	bow_hits = 0
	for i in range(3):
		bow_hits += killJad(gear, True)
	return bow_hits

def killMager(gear = "Task Standard", useBP = True, bp_hp = 50):
	bow_max_hit, bow_accuracy = getDamage(gear, "Mager", "Twisted bow")
	bp_max_hit, bp_accuracy = getDamage(gear, "Mager", "Toxic blowpipe")
	mager = NPC(220)
	bow_hits = 0
	bp_hits = 0
	while mager.hp > bp_hp:
		bow_damage = simHit(bow_accuracy, bow_max_hit)
		mager.lower_hp(bow_damage)
		bow_hits += 1
	while mager.hp < bp_hp and mager.hp > 0:
		if useBP:
			bp_damage = simHit(bp_accuracy, bp_max_hit)
			mager.lower_hp(bp_damage)
			bp_hits += 1
		else:
			bow_damage = simHit(bow_accuracy, bow_max_hit)
			mager.lower_hp(bow_damage)
			bow_hits += 1
	return bow_hits, bp_hits

def killRanger(specs = 2, gear = "Task Standard"):
	bp_max_hit, bp_accuracy = getDamage(gear, "Ranger", "Toxic blowpipe")
	bp_hits = 0
	ranger = NPC(130)
	while ranger.hp > 0:
		if specs > 0:
			bp_damage = simHit(bp_accuracy, int(bp_max_hit * 1.5)) #2 blowpipe specs
			specs -= 1
		else:
			bp_damage = simHit(bp_accuracy, bp_max_hit)
		ranger.lower_hp(bp_damage)
		bp_hits += 1
	return bp_hits

def killHealer(specs = 0, gear = "Task Standard"):
	bp_max_hit, bp_accuracy = getDamage(gear, "Healer", "Toxic blowpipe")
	bp_hits = 0
	healer = NPC(80)
	while healer.hp > 0:
		if specs > 0:
			bp_damage = simHit(bp_accuracy, int(bp_max_hit * 1.5))
			specs -= 1
		else:
			bp_damage = simHit(bp_accuracy, bp_max_hit)
		healer.lower_hp(bp_damage)
		bp_hits += 1
	return bp_hits

def getCombatTime(bow_hits, bp_hits):
	time = 0
	time += bow_hits * 5
	time += bp_hits * 2
	return time

def getZukTime(bow_hits, bp_hits, killedMager = False, killedZukJad = False, killedHealers = False, wasSet = True, unit = "seconds"):
	time = getCombatTime(bow_hits, bp_hits)
	if not killedHealers:
		time += 4 * 2 #Tagging healers
	if wasSet: #If there was a set
		if not killedMager:
			time += 2 #Tagging mager if set spawns
		if not killedZukJad:
			if killedMager:
				time += 2 #Tagging Jad if set spawns
			else:
				time += 3
	else: #Else if no set
		if not killedZukJad:
			time += 2 #Tagging Jad if set doesn't spawn
		elif killedZukJad:
			time += 5 #Tagging Jad healers
	if unit == "seconds":
		time *= 0.6
		time = round(time, 1)
	return time

def format_seconds_to_mmss(seconds, ticks = False):
	if ticks:
		seconds *= 0.6
		seconds = round(seconds, 1)
	minutes = seconds // 60
	seconds %= 60
	return "%02i:%02i" % (minutes, seconds)

def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)

def format_a_over_b_to_percentage(a, b):
	result = a/b
	result *= 100
	result = round(result, 2)
	result = str(result)
	return result

def increment_dict_value(dict, key):
	try:
		dict[key] = dict[key] + 1
	except KeyError:
		dict[key] = 1

def avg(list):
	try:
		return sum(list)/len(list)
	except ZeroDivisionError:
		return 0

def runSim(n, gear, includeMager, includeSingleJad, includeTripleJads, includeZuk, killZukMager, killZukJad, killZukHealers):
	mager_times = []
	single_jad_times = []
	triple_jad_times = []
	zuk_times = []
	set_zuk_times = []
	no_set_zuk_times = []
	zuk_times_dict = {}
	if includeMager:
		for i in range(n):
			bow_hits, bp_hits = killMager(gear, True)
			mager_times.append(getCombatTime(bow_hits, bp_hits))
		mage_average = avg(mager_times)
	else:
		mage_average = -1
	if includeSingleJad:
		for i in range(n):
			bow_hits = killJad(gear)
			single_jad_times.append(getCombatTime(bow_hits, 0))
		single_jad_average = avg(single_jad_times)
	else:
		single_jad_average = -1
	if includeTripleJads:
		for i in range(n):
			bow_hits = killTripleJads(gear)
			triple_jad_times.append(getCombatTime(bow_hits, 0))
		triple_jad_average = avg(triple_jad_times)
	else:
		triple_jad_average = -1
	if includeZuk:
		for i in range(n):
			bowHits, bpHits, wasSet = killZuk(gear, killZukMager, killZukJad, killZukHealers)
			zuk_time = getZukTime(bowHits, bpHits, killZukMager, killZukJad, killZukHealers, wasSet, "ticks")
			zuk_times.append(zuk_time)
			increment_dict_value(zuk_times_dict, zuk_time)
			if wasSet:
				set_zuk_times.append(zuk_time)
			elif not wasSet:
				no_set_zuk_times.append(zuk_time)
		zuk_average = avg(zuk_times)
		set_zuk_average = avg(set_zuk_times)
		no_set_zuk_average = avg(no_set_zuk_times)
	else:
		zuk_average = -1
		set_zuk_average = -1
		no_set_zuk_average = -1
	return mager_times, mage_average, single_jad_times, single_jad_average, triple_jad_average, triple_jad_times, zuk_times, zuk_average, set_zuk_times, set_zuk_average, no_set_zuk_times, no_set_zuk_average, zuk_times_dict



def main(x):
	pass

if __name__ == '__main__':
	main(10000)