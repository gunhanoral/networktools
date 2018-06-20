import ipaddress
import asyncio
import time

now = time.time()

async def check_port(ip, port, loop):
        conn = asyncio.open_connection(ip, port, loop=loop)
        try:
                reader, writer = await asyncio.wait_for(conn, timeout=3)
                return (ip, port, True)
        except:
                return (ip, port, False)

async def check_port_sem(sem, ip, port, loop):
        async with sem:
                return await check_port(ip, port, loop)

async def run(dests, ports, loop):
        sem = asyncio.Semaphore(400) #Change this value for limitation
        tasks = [asyncio.ensure_future(check_port_sem(sem, d, p, loop)) for d in dests for p in ports]
        responses = await asyncio.gather(*tasks)
        return responses

networks = ['1.1.1.0/24', '2.2.2.0/24']
hosts = ['3.3.3.3', '4.4.4.4']

dests = []
for nw in networks:
    for ip in ipaddress.IPv4Network(nw).hosts():
        dests.append(str(ip))

dests.extend(hosts)
ports = [22,23,80,443]

loop = asyncio.get_event_loop()
future = loop.run_until_complete(run(dests, ports, loop))
print('Done. Total time: ', time.time() - now)
print('\n')
for ip, port, res in future:
    print('{}\t{}\t{}'.format(ip,port,res))
