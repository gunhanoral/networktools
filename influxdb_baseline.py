from influxdb import InfluxDBClient
 
# Process data for last X hours
time_period = '72h'
 
all_metrics = [ 'packets_incoming', 'bits_incoming', 'flows_incoming', 'packets_outgoing', 'bits_outgoing', 'flows_outgoing' ]
 
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'fastnetmon')
 
all_hosts = client.query('show tag values from hosts_traffic with key = "host"')
 
all_hosts_dict = {}
 
for point in all_hosts.get_points():
        all_hosts_dict[ point['value'] ] = 1
 
 
print("Extracted", len(all_hosts_dict), "hosts from InfluxDB")
 
query_select_fields = []
 
for metric in all_metrics:
    query_select_fields.append( "max(" + metric + ") as max_" + metric + " " )
 
query_select_field = ",".join(query_select_fields)
 
hosts_to_process = all_hosts_dict.keys()
 
peak_values_across_al_hosts = {}
 
for metrics in all_metrics:
    peak_values_across_al_hosts[ "max_" + metrics] = 0
 
for ix, host in enumerate(hosts_to_process):
    host_metrics = client.query("SELECT " + query_select_field + " FROM hosts_traffic WHERE host = '"+ host + "' AND time >= now() - " + time_period)
    if ix%100 == 0:
        print(ix)
    if host_metrics:   
        for k, v in list(host_metrics.get_points())[0].items():
            if k == "time":
                continue
     
            if peak_values_across_al_hosts[k] < v:
                peak_values_across_al_hosts[k] = v
            # print(k, v)
 
print("Peak values for all your hosts")
for k, v in peak_values_across_al_hosts.items():
    print("{:10} {}".format(k, v))
