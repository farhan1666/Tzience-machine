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
	heal_amount = randint(15,25)
	NPC.heal_hp(heal_amount)

def healJad(NPC, triples = False, zukJad = False):
	pass #I don't know how jad heals work yet

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

def killZuk(gear = "Task Standard", doKillMager = False, doKillHealers = False, doKillJad = False):
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
			else:
				spawnSets = True
		if spawnSets:
			bp_hits += killRanger(2, gear)
			if spec_regen_bp_hits == 0:
				spec_regen_bp_hits = bp_hits - 2
				countSpec = True
			if doKillMager:
				bow_hits_to_kill_mager = killMager(gear, False)[0]
				print(bow_hits_to_kill_mager)
				bow_hits += bow_hits_to_kill_mager
				if countSpec:
					spec_regen_bow_hits += bow_hits_to_kill_mager
			spawnSets = False
		if zuk.hp < 480 and not jadSpawned and doKillJad:
			bow_hits += killJad(gear, False, True)
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
	return bow_hits, bp_hits

def killJad(gear = "Task Standard", triples = False, isZukJad = False):
	bow_max_hit, bow_accuracy = getDamage(gear, "Zuk", "Twisted bow")
	jad = NPC(350)
	bow_hits = 0
	jadHealed = False
	while jad.hp > 0:
		bow_damage = simHit(bow_accuracy, bow_max_hit)
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

def killMager(gear = "Task Standard", useBP = True):
	bow_max_hit, bow_accuracy = getDamage(gear, "Mager", "Twisted bow")
	bp_max_hit, bp_accuracy = getDamage(gear, "Mager", "Toxic blowpipe")
	mager = NPC(220)
	bow_hits = 0
	bp_hits = 0
	while mager.hp > 50:
		bow_damage = simHit(bow_accuracy, bow_max_hit)
		mager.lower_hp(bow_damage)
		bow_hits += 1
	while mager.hp < 50 and mager.hp > 0:
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

def getZukTime(bow_hits, bp_hits, unit = "seconds"):
	time = getCombatTime(bow_hits, bp_hits)
	time += 4 * 2 #Tagging healers
	if bp_hits > 0: #If it wasn't a no set
		time += 2 #Tagging mager if set spawns
		time += 3 #Tagging Jad if set spawns
	else: #Else if no set
		time += 2 #Tagging Jad if set doesn't spawn
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

def increment_dict_value(dict, key):
	try:
		dict[key] = dict[key] + 1
	except KeyError:
		dict[key] = 1

def print_sorted_dict(dict):
	for key in sorted(dict.keys()):
	    print("%s: %s" % (key, dict[key]))

def avg(list):
	return sum(list)/len(list)

def runSim(n, gear, includeMager, includeSingleJad, includeTripleJads, includeZuk, killZukMager, killZukJad, killZukHealers):
	if includeMager:
		mager_times = []
		for i in range(n):
			bow_hits, bp_hits = killMager()
			mager_times.append(getCombatTime(bow_hits, bp_hits))
		mage_average = avg(mager_times)
	else:
		mage_average = -1
	if includeSingleJad:
		single_jad_times = []
		for i in range(n):
			bow_hits = killJad()
			single_jad_times.append(getCombatTime((bow_hits, 0)))
		single_jad_average = avg(single_jad_times)
	else:
		single_jad_average = -1
	if includeTripleJads:
		triple_jad_times = []
		for i in range(n):
			bow_hits = killTripleJads()
			triple_jad_times.append(getCombatTime((bow_hits, 0)))
		triple_jad_average = avg(triple_jad_times)
	else:
		triple_jad_average = -1



def main(x):
	no_set_zuks = []
	set_zuks = []
	no_set_zuk_dict = {}
	set_zuk_dict = {}
	gear = "Task Standard"
	start_time = time.time()
	for i in range(x):
		bowHits, bpHits = killZuk(gear)
		zukTime = getZukTime(bowHits, bpHits, "ticks")
		if bpHits == 0:
			no_set_zuks.append(zukTime)
			increment_dict_value(no_set_zuk_dict, zukTime)
		else:
			set_zuks.append(zukTime)
			increment_dict_value(set_zuk_dict, zukTime)
	elapsed_time = time.time() - start_time
	elapsed_time = format_seconds_to_hhmmss(elapsed_time)

	print("Simulations completed in %s" % (elapsed_time))
	print('%i simulations completed using the \"%s\" gear setup' % (x, gear))
	print("Total No Sets: %i" % (len(no_set_zuks)))
	try:
		print("Average No Set Time:", format_seconds_to_mmss(avg(no_set_zuks), True), "(%i ticks)" % (avg(no_set_zuks)))
	except ZeroDivisionError:
		print("There were 0 No Set Zuks")
	# print_sorted_dict(no_set_zuk_dict)
	try:
		print("Average Set Time:", format_seconds_to_mmss(avg(set_zuks), True), "(%i ticks)" % (avg(set_zuks)))
	except ZeroDivisionError:
		print("There were 0 Set Zuks")
	# print_sorted_dict(set_zuk_dict)
	# input("Press ENTER to end the program.\n")

if __name__ == '__main__':
	main(10000)