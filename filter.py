#!/usr/bin/env python3

import argparse
from scapy.all import *
from netfilterqueue import NetfilterQueue, Packet


def packet_filter(pkt_raw: bytes) -> bool:
    ipv6 = IPv6(pkt_raw)
    return not (TCP in ipv6)


def handle_and_accept(pkt: Packet):
    result = packet_filter(pkt.get_payload())
    if result:
        pkt.accept()
    else:
        pkt.drop()


def setup_nfqueue(nfqueue_num: int, hook: str) -> NetfilterQueue:
    prerouting_cmd = "ip6tables -I %s -t mangle -m ipv6header --soft --header ipv6-route -j NFQUEUE --queue-num %d" % (hook, nfqueue_num)
    subprocess.run(prerouting_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    nfqueue = NetfilterQueue()
    nfqueue.bind(nfqueue_num, handle_and_accept, max_len=2**32-1)
    return nfqueue


def close_nfqueue(nfqueue_num: int, hook: str, nfqueue: NetfilterQueue):
    prerouting_cmd = "ip6tables -D %s -t mangle -m ipv6header --soft --header ipv6-route -j NFQUEUE --queue-num %d" % (hook, nfqueue_num)
    subprocess.run(prerouting_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    nfqueue.unbind()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nfqueue_num", type=int,  default=1, help="nfqueue number")
    parser.add_argument("--hook", type=str, default="PREROUTING", help="nfqueue hook")
    
    args = parser.parse_args()
    return args


def run():
    args = get_args()
    
    nfqueue_num = args.nfqueue_num
    hook = args.hook
    
    nfqueue = setup_nfqueue(nfqueue_num, hook)
    try:
        nfqueue.run()
    except KeyboardInterrupt:
        print("close.")
    
    close_nfqueue(nfqueue_num, hook, nfqueue)


if __name__ == "__main__":
    run()
