import zuk_sim_backend

def main():
	kill_times_but_up_here = []
	kill_times_but_up_here_but_slightly_lower = []
	for i in range(100):
		kill_times = []
		kill_times_but_in_here = []
		for j in range(50000):
			bow_hits, bp_hits = zuk_sim_backend.killMager("Task Standard", True, i)
			bow_hits_2, bp_hits_2 = zuk_sim_backend.killMager("Task Standard", False, i)
			kill_times_but_in_here.append(zuk_sim_backend.getCombatTime(bow_hits_2, bp_hits_2))
			kill_times.append(zuk_sim_backend.getCombatTime(bow_hits, bp_hits))
		kill_times_but_up_here.append(zuk_sim_backend.avg(kill_times))
		kill_times_but_up_here_but_slightly_lower.append(zuk_sim_backend.avg(kill_times_but_in_here))
	print(kill_times_but_up_here.index(min(kill_times_but_up_here)) + 1)
	print()
	for i in range(len(kill_times_but_up_here)):
		print("%i, %.2f" % (i + 1, zuk_sim_backend.avg(kill_times_but_in_here) - kill_times_but_up_here[i]))


if __name__ == '__main__':
	main()