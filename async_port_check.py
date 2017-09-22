import asyncio
import ipaddress
async def check_port(ip, port, loop):
	try:
		reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port, loop=loop), timeout=3)
		writer.close()
		return (ip, port, True)
	except:
		return (ip, port, False)
async def run(dests, ports, loop):
	tasks = [asyncio.ensure_future(check_port(d, p, loop)) for d in dests for p in ports]
	responses = await asyncio.gather(*tasks)
	return responses
dests = ['10.1.1.1', '192.168.1.1', '172.27.3.5']
ports = [21, 22, 23, 80, 443, 3389]
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(dests, ports, loop))
loop.run_until_complete(future)
print('Results: ', future.result())
