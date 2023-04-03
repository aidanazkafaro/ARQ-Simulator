import random
import time
import matplotlib.pyplot as plt

# Mendefinisikan function untuk simulasi Stop and Wait
def simulate_stop_and_wait(packet_size, error_probability, num_packets, bandwidth):
    total_time = 0
    success_transmission = 0
    for i in range(num_packets):
        # Kirim paket
        send_time = time.time()
        if random.random() > error_probability:
            transmission_time = packet_size / bandwidth
            time.sleep(transmission_time)
            total_time += time.time() - send_time
            success_transmission += 1
        else:
            total_time += time.time() - send_time + 2 * packet_size / bandwidth  # Timeout = 2 * RTT

    throughput = success_transmission / total_time
    delay = total_time / num_packets
    return throughput, delay

# Mendefinisikan function untuk simulasi Go back N
def simulate_go_back_n(packet_size, error_probability, num_packets, bandwidth, window_size):
    total_time = 0
    success_transmission = 0
    i = 0
    while i < num_packets:
        # Mengirim paket sebanyak window_size
        window = []
        for j in range(window_size):
            if i + j >= num_packets:
                break
            send_time = time.time()
            window.append((i + j, send_time))
            if random.random() > error_probability:
                transmission_time = packet_size / bandwidth
                time.sleep(transmission_time)
                success_transmission += 1
            else:
                time.sleep(2 * packet_size / bandwidth)  # Timeout = 2 * RTT (Round Trip Time)
                break

        # Terima ACK
        for seq_num, send_time in window:
            if seq_num >= num_packets:
                break
            if random.random() > error_probability:
                transmission_time = packet_size / bandwidth
                time.sleep(transmission_time)
                total_time += time.time() - send_time
            else:
                total_time += time.time() - send_time + 2 * packet_size / bandwidth  # Timeout = 2 * RTT
                i = seq_num
                break
        else:
            i += window_size

    throughput = success_transmission / total_time
    delay = total_time / num_packets
    return throughput, delay


def simulate_selective_repeat(packet_size, error_probability, num_packets, bandwidth, window_size):
    total_time = 0
    success_transmissions = 0
    i = 0
    while i < num_packets:
        # Mengirim paket sebanyak window_size
        window = []
        for j in range(window_size):
            if i + j >= num_packets:
                break
            send_time = time.time()
            window.append((i + j, send_time))
            if random.random() > error_probability:
                transmission_time = packet_size / bandwidth
                time.sleep(transmission_time)
                success_transmissions += 1
            else:
                time.sleep(2 * packet_size / bandwidth)  # Timeout = 2 * RTT (Round Trip Time)

        # Menerima ACK
        for seq_num, send_time in window:
            if seq_num >= num_packets:
                break
            if random.random() > error_probability:
                transmission_time = packet_size / bandwidth
                time.sleep(transmission_time)
                total_time += time.time() - send_time
            else:
                total_time += time.time() - send_time
                success_transmissions += 1

        i += window_size

    throughput = success_transmissions / total_time
    delay = total_time / num_packets
    return throughput, delay


# Mendefine parameter ukuran packet, jumlah packer, bandwidth dan window size
packet_size = 512  # bytes
num_packets = 100
bandwidth = 1e6  # bps
window_size = 10

# Menampilkan interface untuk input user
print("ARQ Simulation Program")
print("Choose ARQ method: \n\n Stop-and-Wait (1) \n Go-back-N (2) \n Selective-Reject (3)\n\n")
user_input = input("Please enter a number between 1 and 3: ")

# Memanggil function berdasarkan input dari user
if user_input == "1":
    # Simulasi Stop-and-Wait
    stop_and_wait_throughputs = []
    stop_and_wait_delays = []
    for error_probability in range(91):
        throughput, delay = simulate_stop_and_wait(packet_size, error_probability / 100, num_packets, bandwidth)
        stop_and_wait_throughputs.append(throughput)
        stop_and_wait_delays.append(delay)

    # Plot hasil simulasi
    error_probs = [i / 100 for i in range(91)]
    plt.plot(error_probs, stop_and_wait_throughputs, label="Stop-and-Wait")
    plt.xlabel("Error Probability")
    plt.ylabel("Throughput (packets/second)")
    plt.legend()
    plt.show()

    plt.plot(error_probs, stop_and_wait_delays, label="Stop-and-Wait")
    plt.xlabel("Error Probability")
    plt.ylabel("Average Delay (seconds)")
    plt.legend()
    plt.show()

elif user_input == "2":
    # Simulasi Go-Back-N
    go_back_n_throughputs = []
    go_back_n_delays = []
    for error_probability in range(91):
        throughput, delay = simulate_go_back_n(packet_size, error_probability / 100, num_packets, bandwidth, window_size)
        go_back_n_throughputs.append(throughput)
        go_back_n_delays.append(delay)

    # Plot hasil simulasi
    error_probs = [i / 100 for i in range(91)]
    plt.plot(error_probs, go_back_n_throughputs, label="Go-Back-N (window_size={})".format(window_size))
    plt.xlabel("Error Probability")
    plt.ylabel("Throughput (packets/second)")
    plt.legend()
    plt.show()

    plt.plot(error_probs, go_back_n_delays, label="Go-Back-N (window_size={})".format(window_size))
    plt.xlabel("Error Probability")
    plt.ylabel("Average Delay (seconds)")
    plt.legend()
    plt.show()

elif user_input == "3":
    # Simulasi Selective Repeat
    selective_repeat_throughputs = []
    selective_repeat_delays = []
    for error_probability in range(91):
        throughput, delay = simulate_selective_repeat(packet_size, error_probability / 100, num_packets, bandwidth,
                                                      window_size)
        selective_repeat_throughputs.append(throughput)
        selective_repeat_delays.append(delay)

    # Plot hasil simulasi
    error_probs = [i / 100 for i in range(91)]
    plt.plot(error_probs, selective_repeat_throughputs, label="Selective Repeat (window_size={})".format(window_size))
    plt.xlabel("Error Probability")
    plt.ylabel("Throughput (packets/second)")
    plt.legend()
    plt.show()

    plt.plot(error_probs, selective_repeat_delays, label="Selective Repeat (window_size={})".format(window_size))
    plt.xlabel("Error Probability")
    plt.ylabel("Average Delay (seconds)")
    plt.legend()
    plt.show()

else:
    print("Invalid input.")


