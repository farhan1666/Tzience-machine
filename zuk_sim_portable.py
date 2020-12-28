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

def healSplat(NPC):
	heal_amount = randint(15,25)
	NPC.heal_hp(heal_amount)

def killZuk(gear = "Task Standard"):
	if gear in ['Task Standard', 'Task Archers', "Task Devout"]:
		bow_max_hit = 83
		bp_max_hit = 34
	elif gear in ['Off Task Standard', 'Off Task Devout']:
		bow_max_hit = 73
		bp_max_hit = 30
	if gear == "Task Standard":
		bow_accuracy = 0.5929
		bp_accuracy = 0.9448
	elif gear == "Task Archers":
		bow_accuracy = 0.6062
		bp_accuracy = 0.9465
	elif gear == "Task Devout":
		bow_accuracy = 0.5712
		bp_accuracy = 0.9419
	elif gear == "Off Task Standard":
		bow_accuracy = 0.5453
		bp_accuracy = 0.9393
	elif gear == "Off Task Devout":
		bow_accuracy = 0.5217
		bp_accuracy = 0.9352
	zuk = NPC(1200)
	ranger = NPC(130)
	bow_hits = 0
	bp_hits = 0
	zukHealed = False
	while zuk.hp > 0: 
		bow_damage = simHit(bow_accuracy, bow_max_hit)
		zuk.lower_hp(bow_damage)
		bow_hits += 1
		if bow_hits == 14:
			if zuk.hp > 600:
				while ranger.hp > 0:
					if bp_hits in [0, 1]:
						bp_damage = simHit(bp_accuracy, int(bp_max_hit * 1.5)) #2 blowpipe specs
					else:
						bp_damage = simHit(bp_accuracy, bp_max_hit)
					ranger.lower_hp(bp_damage)
					bp_hits += 1
		if zuk.hp < 240 and not zukHealed:
			for i in range(7):
				healSplat(zuk)
			zukHealed = True
	return bow_hits, bp_hits

def getZukTime(bow_hits, bp_hits, unit = "seconds"):
	time = 0
	time += bow_hits * 5
	time += bp_hits * 2
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
	print_sorted_dict(no_set_zuk_dict)
	try:
		print("Average Set Time:", format_seconds_to_mmss(avg(set_zuks), True), "(%i ticks)" % (avg(set_zuks)))
	except ZeroDivisionError:
		print("There were 0 Set Zuks")
	print_sorted_dict(set_zuk_dict)
	# input("Press ENTER to end the program.\n")

if __name__ == '__main__':
	main(100000)