import json

def check_overlap(google_res:list,bing_res:list):
    google_res = set(google_res)
    bing_res = set(bing_res)
    # print(google_res)
    # print(bing_res)
    return len(bing_res.intersection(google_res)), list(bing_res.intersection(google_res))

def calculate_rho(google_res:list, bing_res:list):
    overlap = check_overlap(google_res,bing_res)
    if overlap == 1:
        pass

def data_clean(res:str):
    return res.rstrip('/').removeprefix('https://www').removeprefix('http://www').removeprefix("https://").removeprefix(".").removeprefix("http://")

if __name__ == "__main__":

    with open("Bing_Result1.json",'r') as f:
        bing = json.load(f)

    with open("Google_Result1.json",'r') as f:
        google = json.load(f)

    data = {}

    for query in google.keys():
        i = 1
        data[query] = {}
        data[query]['google'] = {}

        for res in google[query]:
            data[query]['google'][data_clean(res)] = i
            i+=1

    for query in bing.keys():
        # data[query]['bing'] = {}
        # for res in bing[query]:
        #     cleaned = data_clean(res)
        #     if cleaned in data[query]['google'].keys():
        #         data[query]['bing'][cleaned] = data[query]['google'][cleaned]
        #     else:
        #         data[query]['bing'][cleaned] = -1

        i = 1
        # data[query] = {}
        data[query]['bing'] = {}

        for res in bing[query]:
            data[query]['bing'][data_clean(res)] = i
            i+=1
        
        data[query]['overlap'], data[query]['matching'] = check_overlap(data[query]['google'].keys(),data[query]['bing'].keys()) 

    
    #Calculating RHO
    for query in google.keys():
        sq_distances = 0
        total_match = len(data[query]['matching'])
        if total_match ==0 :
            rho = 0
        elif total_match == 1:
            rho = 1 if data[query]['google'][data[query]['matching'][0]] == data[query]['bing'][data[query]['matching'][0]] else 0
        else:
            for match in data[query]['matching']:
                sq_distances += (data[query]['google'][match] - data[query]['bing'][match]) ** 2
            
            total_match = len(data[query]['matching'])
            rho = 1 - (6*sq_distances) / (total_match * (  total_match**2 - 1))


        data[query]['rho'] = rho
        
    all_overlap = []
    all_rho = []
    for query in google.keys():
        all_overlap.append(data[query]['overlap'])
        all_rho.append(data[query]['rho'])


    with open("testing_ranks.json","w") as f:
        json.dump(data,f,indent=4)


    print(len(data.keys()))
    print("overlap_avg:", sum(all_overlap)/len(all_overlap))
    print("rho_avg:", sum(all_rho)/len(all_rho))

    final_output = "Queries, Number of Overlapping Results, Percent Overlap, Spearman Coefficient\n"
    i=1
    for query in data.keys():
        final_output += "Query "+str(i) + ", " + str(len(data[query]['matching']))+ ", " + f"{len(data[query]['matching']) * 10.0:.1f}, " + f"{data[query]['rho']:.2f}\n"
        i+=1
    
    final_output += f"Averages, {sum(all_overlap)/len(all_overlap):.2f}, {sum(all_overlap)/len(all_overlap) * 10:.1f}, {sum(all_rho)/len(all_rho):.2f}"

    with open("task2.csv","w") as f:
        f.write(final_output)
    # print(check_overlap(bing["How do you replace coolant thermostat"],google["How do you replace coolant thermostat"]))