import os.path, subprocess
from subprocess import STDOUT,PIPE
from subprocess import check_output
import numpy
import requests
import json
import xml.etree.ElementTree as ET
import csv
import sys 

def BuildCode(nrVehicles, capacity, services, costMatrix, filename):

    code = '''
    import java.io.File;
    import java.util.Collection;

    import com.graphhopper.jsprit.analysis.toolbox.GraphStreamViewer;
    import com.graphhopper.jsprit.analysis.toolbox.GraphStreamViewer.Label;
    import com.graphhopper.jsprit.analysis.toolbox.Plotter;
    import com.graphhopper.jsprit.core.algorithm.VehicleRoutingAlgorithm;
    import com.graphhopper.jsprit.core.algorithm.box.Jsprit;
    import com.graphhopper.jsprit.core.problem.Location;
    import com.graphhopper.jsprit.core.problem.VehicleRoutingProblem;
    import com.graphhopper.jsprit.core.problem.VehicleRoutingProblem.FleetSize;
    import com.graphhopper.jsprit.core.problem.cost.VehicleRoutingTransportCosts;
    import com.graphhopper.jsprit.core.problem.job.Service;
    import com.graphhopper.jsprit.core.problem.solution.VehicleRoutingProblemSolution;
    import com.graphhopper.jsprit.core.problem.vehicle.VehicleImpl;
    import com.graphhopper.jsprit.core.problem.vehicle.VehicleType;
    import com.graphhopper.jsprit.core.problem.vehicle.VehicleTypeImpl;
    import com.graphhopper.jsprit.core.reporting.SolutionPrinter;
    import com.graphhopper.jsprit.core.util.Solutions;
    import com.graphhopper.jsprit.core.util.VehicleRoutingTransportCostsMatrix;
    import com.graphhopper.jsprit.io.problem.VrpXMLWriter;

    /**
     * @author Francesco
     * creato il 10/nov/2017 14:59:56
     */
    public class '''+ filename +''' {

          public static void main(String[] args) {
                /*
                 * some preparation - create output folder
                 */
                File dir = new File("output");
                // if the directory does not exist, create it
                if (!dir.exists()) {
                    System.out.println("creating directory ./output");
                    boolean result = dir.mkdir();
                    if (result) System.out.println("./output created");
                }


                int vehiclesNumber = '''+str(nrVehicles)+''';
                int capacity = '''+str(capacity)+''';

                /*
                 * get a vehicle type-builder and build a type with the typeId "vehicleType" and one capacity dimension, i.e. weight, and capacity dimension value of 2
                 */
                final int WEIGHT_INDEX = 0;

                VehicleTypeImpl.Builder vehicleTypeBuilder = VehicleTypeImpl.Builder.newInstance("vehicleType").addCapacityDimension(WEIGHT_INDEX, capacity);
                VehicleType vehicleType = vehicleTypeBuilder.build();

                VehicleRoutingProblem.Builder vrpBuilder = VehicleRoutingProblem.Builder.newInstance();
                vrpBuilder.setFleetSize(FleetSize.FINITE);

                for(int i = 0; i < vehiclesNumber; i++) {
                    String vehicleId = "Vehicle_" + i;
                    VehicleImpl.Builder vehicleBuilder = VehicleImpl.Builder.newInstance(vehicleId);
                    vehicleBuilder.setStartLocation(Location.newInstance(0));
                    vehicleBuilder.setType(vehicleType);
                    VehicleImpl vehicle = vehicleBuilder.build();
                    vrpBuilder.addVehicle(vehicle);
                }

                \n''' + costMatrix + '''\n

                /*
                 * build services at the required locations, each with a capacity-demand of 1.
                 */

            \n''' + services + '''\n

                VehicleRoutingTransportCosts costMatrix = costMatrixBuilder.build();

                vrpBuilder.setRoutingCost(costMatrix);

                VehicleRoutingProblem problem = vrpBuilder.build();

                /*
                 * get the algorithm out-of-the-box.
                 */
                VehicleRoutingAlgorithm algorithm = Jsprit.createAlgorithm(problem);

                /*
                 * and search a solution
                 */
                Collection<VehicleRoutingProblemSolution> solutions = algorithm.searchSolutions();

                /*
                 * get the best
                 */
                VehicleRoutingProblemSolution bestSolution = Solutions.bestOf(solutions);

                new VrpXMLWriter(problem, solutions).write("output/problem-with-solution.xml");

                SolutionPrinter.print(problem, bestSolution, SolutionPrinter.Print.VERBOSE);

            }

        }
        '''
    with open(filename + '.java', 'w') as the_file:
        the_file.write(code)
      
def compile_java(java_file):
    lib='.:./libs/*'
    if sys.platform == 'win32':
        lib='.;./libs/*'
    subprocess.check_call(['javac', '-cp', lib, java_file])

def execute_java(java_file):
    java_class,ext = os.path.splitext(java_file)
    lib='.:./libs/*'
    if sys.platform == 'win32':
        lib='.;./libs/*'
    cmd = ['java', '-cp', lib, java_class]
    #proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='utf8')
    try:
        ans = check_output(['java', '-cp', lib, java_class])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    #stdout,stderr = proc.communicate(stdin)
    solution = ans.decode("utf8")
    print(solution)

    if "solution" in solution:
        route, costs = parseXML("output/problem-with-solution.xml")
        print(route)
        print(costs)
    return route, costs

    #print ('This was "' + stdout + '"')

def GenerateCoordinates(nrClients):
    N = 39.33
    S = 38.9669
    O = 16.31
    E = 16.98

    lats = numpy.random.uniform(S, N, size=nrClients)
    lons = numpy.random.uniform(O, E, size=nrClients)

    #print("Coordinate deposito: "+ lats[0] + ", "+ lons[0])
    return lats, lons


def BuildClients(lats, lons, IDcliente):

    deposito = (38.926, 16.4857)

    clienti = {0: deposito}

    for i in range(len(lats)):
        clienti[IDcliente] = (lats[i], lons[i])
        IDcliente += 1

    print(clienti)
    return clienti, IDcliente


def Merge(clienti1, clienti2):
    res = {**clienti1, **clienti2}
    return res

def BuildDistanceGraph(clienti1, clienti2):

    clienti = Merge(clienti1, clienti2)

    params = (('access_token', 'pk.eyJ1IjoiZmx1bmljYWwiLCJhIjoiY2p3cnhnNTUzMDNqMTN5bzJ4cGhhYXVlbSJ9.cQBQ_HN7wFXRWO4cjVph3Q'),)

    DG = {} # Distance Graph

    for index1, coord1 in clienti.items():
        for index2, coord2 in clienti.items():
            if index1 < index2:
                response = requests.get(
                    "https://api.mapbox.com/optimized-trips/v1/mapbox/driving/" + str(coord1[1]) + "," + str(
                        coord1[0]) + ";" + str(coord2[1]) + "," + str(coord2[0]), params=params)
                json_data = json.loads(response.text)
                #print(json_data)
                #distance = float(json_data['trips'][0]['distance'])
                distance = float(json_data['trips'][0]['legs'][0]['distance'])
                DG[(index1, index2)] = distance * 0.001
    print("=============DG==================")         
    print(DG)

    return DG


    # for i in range(len(lats) - 1):
    #     print("(" + str(lats[i + 1]) + "," + str(lons[i + 1]) + ")")
    #     for j in range(i + 1, len(lats)):
    #         response = requests.get("https://api.mapbox.com/optimized-trips/v1/mapbox/driving/" + str(lons[i]) + "," + str(lats[i]) + ";" + str(lons[j]) + "," + str(lats[j]), params=params)
    #         json_data = json.loads(response.text)
    #         # distance = float(json_data['trips'][0]['distance'])
    #         distance = float(json_data['trips'][0]['legs'][0]['distance'])
    #
    #         A[i][j] = distance * 0.001
    #
    # printMatrix(A)


def exchange_candidates(routes_s1, routes_s2, clienti1, DG):

    candidates = []

    #customers_positions_s1 = shipper1[0]

    #customers_demands_s1 = shipper1[1]

    #routes_s1 = route1
    # depot_cords_s1 = shipper1[-1]

    #routes_s2 = route2

    residual_vehicles_capacity_2_s2 = {"Vehicle_0" : 10000000000000, "Vehicle_1" : 10000000000000} #shipper2[4]

    for cliente in clienti1.keys():

        if cliente == 0: # deposito skip
            continue

        demand = 1
        candidate_routes_ids = []

       # IDcliente_i = position # IDsClienti.get(customer)

        for i in range(len(routes_s2)):
            vehicle = routes_s2[i][1]
            if residual_vehicles_capacity_2_s2[vehicle] >= demand:
                candidate_routes_ids.append(i)

        if len(candidate_routes_ids) > 0:
            min_delta_i, best_route_s2, index_i_route_s2 = compute_min_delta_i(cliente, routes_s2, candidate_routes_ids, DG)
        else:
            #print("Impossibile scambiare " + customer)
            #print("La sua domanda supera la capacità residua di tutti i veicoli dell'altro shipper!")
            continue

        route = None

        for rv in routes_s1:   # tuple route, vehicle
            if str(cliente) in rv[0]:
                route = rv[0]
                break

        saving_i_r1 = compute_savings_i(cliente, route, DG)

        gain = saving_i_r1 - min_delta_i

        print("")
        print("Customer: " + str(cliente) + " saving: " + str(saving_i_r1) + "delta: " + str(min_delta_i) + " gain: " + str(saving_i_r1-min_delta_i))
        print("")

        if gain > 0:
            candidates.append((cliente, route, best_route_s2, index_i_route_s2, gain, saving_i_r1, min_delta_i))

    return candidates


def compute_savings_i(cliente_i, route, DG):   # passare la coordinata x come LON e la coordinata y come LAT

    x_i = cliente_i
    x_d = 0

    i_index = route.index(str(x_i))

    if len(route) > 1:
        if i_index == 0:
            x_s = x_d

            x_e = int(route[i_index + 1])

        elif i_index == len(route) - 1:
            x_s = int(route[i_index - 1]) # x cord
            x_e = x_d

        else:
            x_s = int(route[i_index - 1])  # x cord
            x_e = int(route[i_index + 1])

        s_e_cost = DG[(x_e,x_s)] if x_e < x_s else DG[(x_s,x_e)]  # math.hypot(x_e - x_s, y_e - y_s)
        s_i_cost = DG[(x_i,x_s)] if x_i < x_s else DG[(x_s,x_i)]  # math.hypot(x_i - x_s, y_i - y_s)
        i_e_cost = DG[(x_e,x_i)] if x_e < x_i else DG[(x_i,x_e)]  # math.hypot(x_e - x_i, y_e - y_i)
        saving_i = s_i_cost + i_e_cost - s_e_cost

    else:   saving_i = DG[(x_d,x_i)] if DG[(x_d,x_i)] > 0 else DG[(x_i,x_d)] # math.hypot(x_d - x_i, y_d - y_i)

    return saving_i


def compute_min_delta_i(cliente_i, routes_2, candidate_routes_ids, DG):

    #routes_2 = route2

    x_d = 0
    x_i = cliente_i

    min_delta_i = 2 ** 10000

    best_route = None

    index_i_route_s2 = -1

    for j in candidate_routes_ids:

        route = routes_2[j][0]

        for l in range(len(route)):

            if l == 0:
                x_s = x_d
                x_e = int(route[l])

            elif l == len(route) - 1:
                x_s = int(route[l])  # x cord
                x_e = x_d

            else:
                x_s = int(route[l-1])  # x cord
                x_e = int(route[l])

            s_e_cost = DG[(x_e,x_s)] if x_e < x_s else DG[(x_s,x_e)]  # math.hypot(x_e - x_s, y_e - y_s)
            s_i_cost = DG[(x_i,x_s)] if x_i < x_s else DG[(x_s,x_i)] # math.hypot(x_i - x_s, y_i - y_s)
            i_e_cost = DG[(x_e,x_i)] if x_e < x_i else DG[(x_i,x_e)] # math.hypot(x_e - x_i, y_e - y_i)

            w = s_i_cost + i_e_cost - s_e_cost

            if w < min_delta_i:
                min_delta_i = w
                best_route = route
                index_i_route_s2 = l

    return min_delta_i, best_route, index_i_route_s2


def exchange(candidates, routes_2):

    ordered_candidates = sorted(candidates, key=lambda x: x[4])
    #routes_2 = route2

    customers_to_move = []

    total_saving_s1 = 0
    total_additional_cost_s2 = 0

    assigned_routes = [False]*len(routes_2)

    print("###################")
    print("Customers scambiati")
    print("")

    used_routes_1 = []

    for candidate in reversed(ordered_candidates):
        customer = candidate[0]
        route = candidate[1]
        best_route_s2 = candidate[2]
        index_i_route_s2 = candidate[3]
    #    gain = candidate[4]
        saving_i_r1 = candidate[5]
        min_delta_i = candidate[6]

        # print("Customer: " + customer + " è candidato ad essere inserito nella rotta " + str(best_route_s2))
        #
        # if index_i_route_s2 > 0 and index_i_route_s2 < len(best_route_s2) - 1:
        #     print("In particolare, la posizione di inserimento sarebbe tra i nodi " + str(best_route_s2[index_i_route_s2 - 1]) + " e " + str(best_route_s2[index_i_route_s2]))
        # elif index_i_route_s2 == 0:
        #     print("In particolare, la posizione di inserimento sarebbe tra i nodi deposito e " + str(best_route_s2[index_i_route_s2]))
        # else:
        #     print("In particolare, la posizione di inserimento sarebbe tra i nodi " + str(best_route_s2[index_i_route_s2]) + " e deposito.")

        print("")
        for j in range(len(routes_2)):
            if best_route_s2 in routes_2[j] and not assigned_routes[j] and route not in used_routes_1:
                used_routes_1.append(route)
                assigned_routes[j] = True
                customers_to_move.append(customer)
                total_saving_s1 += saving_i_r1
                total_additional_cost_s2 += min_delta_i
                print("Customer: " + str(customer) + " sarà inserito nella rotta " + str(best_route_s2))
                if index_i_route_s2 > 0 and index_i_route_s2 < len(best_route_s2) - 1:
                    print("In particolare, la posizione di inserimento è tra i nodi " + str(best_route_s2[index_i_route_s2 - 1]) + " e " + str(best_route_s2[index_i_route_s2]))
                elif index_i_route_s2 == 0:
                    print("In particolare, la posizione di inserimento è tra i nodi deposito e " + str(best_route_s2[index_i_route_s2]))
                else:
                    print("In particolare, la posizione di inserimento è tra i nodi " + str(best_route_s2[index_i_route_s2]) + " e deposito.")
                break
    print("###################")
    print("")
    return customers_to_move, total_saving_s1, total_additional_cost_s2



def printMatrix(m):
    """Stampa in output una matrice allineando opportunamente"""
    #trasformiamo tutto in stringhe e calcoliamo la stringa più lunga
    lMax=0
    ms = []
    for i in range(len(m)):
        riga = []
        for j in range(len(m[i])):
            s = str(m[i][j])
            if len(s) > lMax :
                lMax = len(s)
            riga.append(s)
        ms.append(riga)
    #stampiamo allineando a destra in un campo grande lMax
    for i in range(len(ms)):
        print("|",end="")
        for j in range(len(ms[i])):
            print(ms[i][j].rjust(lMax+1),end="")
        print("|")

def strip_bad_strings(solution_shipper_path):

    string_1 = '<problem xmlns="http://www.w3schools.com"\n'
    string_2 = '     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.w3schools.com vrp_xml_schema.xsd">\n'

    lines = []
    with open(solution_shipper_path) as infile:
        for line in infile:
            if "<problem" in line:
                line = line.replace(string_1, "<problem")
            elif "xmlns:xsi" in line:
                line = line.replace(string_2, ">\n")
            lines.append(line)

    with open(solution_shipper_path, 'w') as outfile:
        for line in lines:
            outfile.write(line)

def parseXML(xmlfile):
    # create element tree object
    strip_bad_strings(xmlfile)

    tree = ET.parse(xmlfile)

    # get root element
    root = tree.getroot()

    optimal_cost = 1000000000
    routes2 = []
    costs2 = []

    for solution in root.findall('solutions/solution'):
        cost = float(solution.find('cost').text)

        if cost < optimal_cost:

            routes2 = []
            costs2 = []
            optimal_cost = cost
            rotte = solution.find('routes')
            #print(cost)
            for route in rotte:
                # print(service.get('id'))
                activities = []
                weight = 0
                vehicle = route.find('vehicleId').text

                for act in route.findall('act'):
                    a = act.find('serviceId').text
                    activities.append(a)
                    #weight += float(demands[a])

                if activities not in routes2:
                    routes2.append((activities, vehicle))
                    costs2.append(float(route.find('end').text))
        return routes2, cost

def run2():

    noc1 = 10
    noc2 = 5
    clienti1, lastIdCliente = GenerateCoordinates(noc1, 1)
    clienti2, lastIdCliente = GenerateCoordinates(noc2, lastIdCliente)

    DG = BuildDistanceGraph(clienti1, clienti2)
    BuildProblem(2, 100, clienti1, DG, "Test1")
    BuildProblem(2, 100, clienti2, DG, "Test2")

    compile_java('Test1.java')
    compile_java('Test2.java')
    route1, cost1 = execute_java('Test1.java')
    route2, cost2 = execute_java('Test2.java')
    print(route1, cost1)
    print(route2, cost2)
    # return route, costs

    #return clienti1, clienti2, DG

def solve():
    compile_java('Test1.java')
    compile_java('Test2.java')
    route1, cost1 = execute_java('Test1.java')
    route2, cost2 = execute_java('Test2.java')
    return [(route1, cost1), (route2, cost2)]

def prepare_problem(customers_to_move, clienti1, clienti2):
    for IndexCliente in customers_to_move:
        cliente = clienti1.pop(IndexCliente)
        clienti2[IndexCliente] = cliente

def BuildProblem(NrVehicles, capacity, clienti, DG, filename):

    costMatrix = '''\t\t\t\tVehicleRoutingTransportCostsMatrix.Builder costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(true);\n'''

    services = ""
    for index1, coord1 in clienti.items():
        if index1 > 0:
            services += '''\t\t\t\tvrpBuilder.addJob(Service.Builder.newInstance("'''+str(index1)+'''").addSizeDimension(WEIGHT_INDEX, 1).setLocation(Location.newInstance("'''+str(index1)+'''")).build());\n'''
        for index2, coord2 in clienti.items():
            if index1 < index2:
                costMatrix += '''\t\t\t\tcostMatrixBuilder.addTransportDistance("''' + str(index1) + '''", "''' + str(index2) + '''", ''' + str(DG[(index1, index2)]) + ''');''' + "\n"

    # print(services)
    # print(costMatrix)


    BuildCode(NrVehicles, capacity, costMatrix, services, filename)


#run()

def alternate():
    while True:
        yield 0
        yield 1

def run(noc1, noc2):
    lats1, lons1 = GenerateCoordinates(noc1)
    clienti1, lastIdCliente = BuildClients(lats1, lons1, 1)
    lats2, lons2 = GenerateCoordinates(noc2)
    clienti2, lastIdCliente = BuildClients(lats2, lons2, lastIdCliente)

    return [clienti1, clienti2, noc1, noc2]

def demo(noc1, noc2):

    clienti = run(noc1, noc2)
    #print(clienti)
    DG = BuildDistanceGraph(clienti[0], clienti[1])
    BuildProblem(2, 100, clienti[0], DG, "Test1")
    BuildProblem(2, 100, clienti[1], DG, "Test2")
    s = solve()

    return clienti, s

def cooperation(clienti1, clienti2):
    customers_to_move, total_saving_s1, total_additional_cost_s2 = [], 0, 0
    lb_s1 = 0
    ub_s2 = 0

    noc1 = len(clienti1) - 1
    noc2 = len(clienti2) - 1
    clienti = [clienti1, clienti2]

    DG = BuildDistanceGraph(clienti[0], clienti[1])
    BuildProblem(2, 100, clienti[0], DG, "Test1")
    BuildProblem(2, 100, clienti[1], DG, "Test2")

    steps = 6
    i = 0

    x = alternate()

    s1_sol = -1
    s2_sol = -1

    s1 = 0
    s2 = 0

    z1 = 0
    z2 = 0

    old_z1 = 0
    old_z2 = 0

    route1 = []
    route2 = []

    output_file_name = "result_"+str(noc1)+"_"+str(noc2)

    with open(output_file_name, 'w') as csvfile:

        myFields = ['step', 'nor1', 'nor2', 'nos', 'saving', 'delta', 'gain', 'z1', 'z2', 'ztot', 'zgain', 'ez1', 'ez2', 'eztot']
        writer = csv.DictWriter(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, fieldnames=myFields)
        writer.writeheader()

        while i < steps:

            #spaths = ["/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_1_step_" + str(i) + "-with-solution.xml", "/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_2_step_" + str(i) + "-with-solution.xml"]

          #  strip_bad_strings(spaths[0])
          #  strip_bad_strings(spaths[1])

            solutions = solve()

            s1 = x.__next__()
            s2 = x.__next__()

            route1, cost1 = solutions[s1]
            route2, cost2 = solutions[s2]

            clienti1 = clienti[s1]
            clienti2 = clienti[s2]

            #print_problems_settings(shipper1, shipper2)

            z1 = cost1          # sum(cost for cost in shipper1[3])
            z2 = cost2          # sum(cost for cost in shipper2[3])

            if s1_sol == -1:
                s1_sol = z1

            if s2_sol == -1:
                s2_sol = z2

            print("After step:" + str(i))
            print("Individual total cost of Shipper " + str(s1+1) + ": " + str(z1))
            print("Individual total cost of Shipper " + str(s2+1) + ": "+  str(z2))
            print("Costs SUM: " + str(z1+z2))

            print("")
            print("")

            if i == 0:
                writer.writerow({'step': str(i), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': '0', 'saving': '0',
                                 'delta': '0', 'gain': '0',
                                 'z1': str(z1).replace('.',','), 'z2': str(z2).replace('.',','), 'ztot': str(z1 + z2).replace('.',','), 'zgain':'0', 'ez1': '0', 'ez2': '0',
                                 'eztot': '0'})
                old_z1 = z1
                old_z2 = z2
                print("Starting cooperation...")

            elif i%2 == 1:
                writer.writerow({'step': str(i), 'nor1': str(len(route2)), 'nor2': str(len(route1)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.',','), 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z2).replace('.', ','),
                                 'z2': str(z1).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','), 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','), 'ez1': str(lb_s1).replace('.', ','), 'ez2': str(ub_s2).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
                old_z1 = z2
                old_z2 = z1

            else:
                writer.writerow({'step': str(i), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.',','), 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z1).replace('.', ','),
                                 'z2': str(z2).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','), 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','), 'ez1': str(ub_s2).replace('.', ','), 'ez2': str(lb_s1).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.',',')})
                old_z1 = z1
                old_z2 = z2

            print("Exchanging customers from " + str(s1+1) + " to " + str(s2+1))
            print("")

            candidates = exchange_candidates(route1, route2,  clienti1, DG)

            #print(candidates)

            # non c'è bisogno di restituire le posizioni dei customers nelle rotte di S2 perché al prossimo passo riutilizzo JSPRIT per calcolare le soluzioni ottime
            # dunque dovrò semplicemente inserire i customer nel grafo di S2 e rimuoverli da quello di S1

            customers_to_move, total_saving_s1, total_additional_cost_s2 = exchange(candidates, route2)

            print("")

            if len(customers_to_move) > 0:
                print("List of " + str(s1+1) + "'s customers ready to go!")
                print(str(customers_to_move))
            else:
                print("No more exchanges available. All of the gains are negative!\nQuitting...")
                break

            print("")

            lb_s1 = z1 - total_saving_s1
            ub_s2 = z2 + total_additional_cost_s2

            print("Lower bound on " + str(s1+1) + " optimal solution: " + str(lb_s1))
            print("Upper bound on " + str(s2+1) + " total cost: " + str(ub_s2))
            print("")

            print("Costs SUM after cooperation (Upper bound): " + str(lb_s1 + ub_s2))

            print("Total gain after cooperation (Lower bound): " + str(z1 + z2 - lb_s1 - ub_s2))

            i += 1

            x.__next__()


            # if s1 == 0:
            prepare_problem(customers_to_move, clienti1, clienti2)
            # else:
            #     prepare_problem(customers_to_move, clienti2, clienti1)
            if s1 == 0:
                BuildProblem(2, 100, clienti1, DG, "Test1")
                BuildProblem(2, 100, clienti2, DG, "Test2")
            else:
                BuildProblem(2, 100, clienti2, DG, "Test1")
                BuildProblem(2, 100, clienti1, DG, "Test2")


            # if s1 == 0:
            #     create_graphs(customers_to_move, shipper1, shipper2, 1, 2, nov, d_cords, capacity, i)
            # else:
            #     create_graphs(customers_to_move, shipper1, shipper2, 2, 1, nov, d_cords, capacity, i)

        print("")
        print("#####################################################")
        print("Summary.")
        print("")
        print("Initial solution values:")
        print("S1 optimal cost --> " + str(s1_sol))
        print("S2 optimal cost --> " + str(s2_sol))
        print("Sum of costs --> " + str(s1_sol + s2_sol))
        print("")

        risultato = str(s1_sol)+";"+str(s2_sol)

        if i == steps:
            # subprocess.check_call(['java', '-jar', './libs/Solver.jar', str(i), '1'], stdout=subprocess.DEVNULL)
            # subprocess.check_call(['java', '-jar', './libs/Solver.jar', str(i), '2'], stdout=subprocess.DEVNULL)
            #
            # spaths = ["/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_1_step_" + str(
            #     i) + "-with-solution.xml",
            #           "/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_2_step_" + str(
            #               i) + "-with-solution.xml"]
            #
            # strip_bad_strings(spaths[0])
            # strip_bad_strings(spaths[1])
            #
            # s1 = x.__next__()
            # s2 = x.__next__()
            #
            # shipper1 = parseXML(spaths[s1])
            # shipper2 = parseXML(spaths[s2])
            #
            # z1 = sum(cost for cost in shipper1[3])
            # z2 = sum(cost for cost in shipper2[3])

            solutions = solve()

            s1 = x.__next__()
            s2 = x.__next__()

            route1, cost1 = solutions[s1]
            route2, cost2 = solutions[s2]

            # clienti1 = clienti[s1]
            # clienti2 = clienti[s2]

            #print_problems_settings(shipper1, shipper2)

            z1 = cost1          # sum(cost for cost in shipper1[3])
            z2 = cost2          # sum(cost for cost in shipper2[3])

            print("Solution values after cooperation (" + str(steps) + " steps):")

            if i%2==0:
                writer.writerow({'step': str(steps), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.', ','),
                                 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z1).replace('.', ','),
                                 'z2': str(z2).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','),
                                 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','),
                                 'ez1': str(ub_s2).replace('.', ','), 'ez2': str(lb_s1).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
            else:
                writer.writerow({'step': str(steps), 'nor1': str(len(route2)), 'nor2': str(len(route1)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.', ','),
                                 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z2).replace('.', ','),
                                 'z2': str(z1).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','),
                                 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','),
                                 'ez1': str(lb_s1).replace('.', ','), 'ez2': str(ub_s2).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
        else:
            print("Solution values after cooperation (" + str(i) + " steps):")

        s1opt = 0
        s2opt = 0

        if s1 == 0:
            print("S1 optimal cost --> " + str(z1))
            print("S2 optimal cost --> " + str(z2))
            s1opt = z1
            s2opt = z2
        else:
            print("S1 optimal cost --> " + str(z2))
            print("S2 optimal cost --> " + str(z1))
            s2opt = z1
            s1opt = z2
            clienti1 = clienti[1]
            clienti2 = clienti[0]

        print("Sum of costs --> " + str(z1 + z2))

        print("Cooperation gain --> " + str((s1_sol + s2_sol) - (z1 + z2)))

        print(route1, route2, s1opt, s2opt)

        risultato += ";" + str((s1_sol + s2_sol) - (z1 + z2)) + ";" + str(i)

        #risultato = {sol_s1_iniziale; sol_s2_iniziale; gain; steps}

        value = {'clienti1' : clienti1, 'clienti2' : clienti2, 'rotta1' : route1, 'costo1' : s1opt, 'rotta2' : route2, 'costo2' : s2opt, 'risultato': risultato}

        return value

def upload(clienti):  
    DG = BuildDistanceGraph(clienti[0], clienti[1])
    BuildProblem(2, 100, clienti[0], DG, "Test1")
    BuildProblem(2, 100, clienti[1], DG, "Test2")
    s = solve()

    return clienti, s


def main():
    customers_to_move, total_saving_s1, total_additional_cost_s2 = [], 0, 0
    lb_s1 = 0
    ub_s2 = 0
    noc1 = 10
    noc2 = 5
    p = run(noc1, noc2)

    clienti = [p[0], p[1]]
    noc1 = p[2]
    noc2 = p[3]

    DG = BuildDistanceGraph(clienti[0], clienti[1])
    BuildProblem(2, 100, clienti[0], DG, "Test1")
    BuildProblem(2, 100, clienti[1], DG, "Test2")

    steps = 6
    i = 0

    x = alternate()

    s1_sol = -1
    s2_sol = -1

    s1 = 0
    s2 = 0

    z1 = 0
    z2 = 0

    old_z1 = 0
    old_z2 = 0

    route1 = []
    route2 = []

    output_file_name = "result_"+str(noc1)+"_"+str(noc2)

    with open(output_file_name, 'w') as csvfile:

        myFields = ['step', 'nor1', 'nor2', 'nos', 'saving', 'delta', 'gain', 'z1', 'z2', 'ztot', 'zgain', 'ez1', 'ez2', 'eztot']
        writer = csv.DictWriter(csvfile, delimiter=';', quoting=csv.QUOTE_NONE, fieldnames=myFields)
        writer.writeheader()

        while i < steps:

            #spaths = ["/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_1_step_" + str(i) + "-with-solution.xml", "/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_2_step_" + str(i) + "-with-solution.xml"]

          #  strip_bad_strings(spaths[0])
          #  strip_bad_strings(spaths[1])

            solutions = solve()

            s1 = x.__next__()
            s2 = x.__next__()

            route1, cost1 = solutions[s1]
            route2, cost2 = solutions[s2]

            clienti1 = clienti[s1]
            clienti2 = clienti[s2]

            #print_problems_settings(shipper1, shipper2)

            z1 = cost1          # sum(cost for cost in shipper1[3])
            z2 = cost2          # sum(cost for cost in shipper2[3])

            if s1_sol == -1:
                s1_sol = z1

            if s2_sol == -1:
                s2_sol = z2

            print("After step:" + str(i))
            print("Individual total cost of Shipper " + str(s1+1) + ": " + str(z1))
            print("Individual total cost of Shipper " + str(s2+1) + ": "+  str(z2))
            print("Costs SUM: " + str(z1+z2))

            print("")
            print("")

            if i == 0:
                writer.writerow({'step': str(i), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': '0', 'saving': '0',
                                 'delta': '0', 'gain': '0',
                                 'z1': str(z1).replace('.',','), 'z2': str(z2).replace('.',','), 'ztot': str(z1 + z2).replace('.',','), 'zgain':'0', 'ez1': '0', 'ez2': '0',
                                 'eztot': '0'})
                old_z1 = z1
                old_z2 = z2
                print("Starting cooperation...")

            elif i%2 == 1:
                writer.writerow({'step': str(i), 'nor1': str(len(route2)), 'nor2': str(len(route1)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.',','), 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z2).replace('.', ','),
                                 'z2': str(z1).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','), 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','), 'ez1': str(lb_s1).replace('.', ','), 'ez2': str(ub_s2).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
                old_z1 = z2
                old_z2 = z1

            else:
                writer.writerow({'step': str(i), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.',','), 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z1).replace('.', ','),
                                 'z2': str(z2).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','), 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','), 'ez1': str(ub_s2).replace('.', ','), 'ez2': str(lb_s1).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.',',')})
                old_z1 = z1
                old_z2 = z2

            print("Exchanging customers from " + str(s1+1) + " to " + str(s2+1))
            print("")

            candidates = exchange_candidates(route1, route2,  clienti1, DG)

            #print(candidates)

            # non c'è bisogno di restituire le posizioni dei customers nelle rotte di S2 perché al prossimo passo riutilizzo JSPRIT per calcolare le soluzioni ottime
            # dunque dovrò semplicemente inserire i customer nel grafo di S2 e rimuoverli da quello di S1

            customers_to_move, total_saving_s1, total_additional_cost_s2 = exchange(candidates, route2)

            print("")

            if len(customers_to_move) > 0:
                print("List of " + str(s1+1) + "'s customers ready to go!")
                print(str(customers_to_move))
            else:
                print("No more exchanges available. All of the gains are negative!\nQuitting...")
                break

            print("")

            lb_s1 = z1 - total_saving_s1
            ub_s2 = z2 + total_additional_cost_s2

            print("Lower bound on " + str(s1+1) + " optimal solution: " + str(lb_s1))
            print("Upper bound on " + str(s2+1) + " total cost: " + str(ub_s2))
            print("")

            print("Costs SUM after cooperation (Upper bound): " + str(lb_s1 + ub_s2))

            print("Total gain after cooperation (Lower bound): " + str(z1 + z2 - lb_s1 - ub_s2))

            i += 1

            x.__next__()


            # if s1 == 0:
            prepare_problem(customers_to_move, clienti1, clienti2)
            # else:
            #     prepare_problem(customers_to_move, clienti2, clienti1)
            if s1 == 0:
                BuildProblem(2, 100, clienti1, DG, "Test1")
                BuildProblem(2, 100, clienti2, DG, "Test2")
            else:
                BuildProblem(2, 100, clienti2, DG, "Test1")
                BuildProblem(2, 100, clienti1, DG, "Test2")


            # if s1 == 0:
            #     create_graphs(customers_to_move, shipper1, shipper2, 1, 2, nov, d_cords, capacity, i)
            # else:
            #     create_graphs(customers_to_move, shipper1, shipper2, 2, 1, nov, d_cords, capacity, i)

        print("")
        print("#####################################################")
        print("Summary.")
        print("")
        print("Initial solution values:")
        print("S1 optimal cost --> " + str(s1_sol))
        print("S2 optimal cost --> " + str(s2_sol))
        print("Sum of costs --> " + str(s1_sol + s2_sol))
        print("")

        if i == steps:
            # subprocess.check_call(['java', '-jar', './libs/Solver.jar', str(i), '1'], stdout=subprocess.DEVNULL)
            # subprocess.check_call(['java', '-jar', './libs/Solver.jar', str(i), '2'], stdout=subprocess.DEVNULL)
            #
            # spaths = ["/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_1_step_" + str(
            #     i) + "-with-solution.xml",
            #           "/Users/flupia/PycharmProjects/next_shop_5.2/output/instance_problem_2_step_" + str(
            #               i) + "-with-solution.xml"]
            #
            # strip_bad_strings(spaths[0])
            # strip_bad_strings(spaths[1])
            #
            # s1 = x.__next__()
            # s2 = x.__next__()
            #
            # shipper1 = parseXML(spaths[s1])
            # shipper2 = parseXML(spaths[s2])
            #
            # z1 = sum(cost for cost in shipper1[3])
            # z2 = sum(cost for cost in shipper2[3])

            solutions = solve()

            s1 = x.__next__()
            s2 = x.__next__()

            route1, cost1 = solutions[s1]
            route2, cost2 = solutions[s2]

            # clienti1 = clienti[s1]
            # clienti2 = clienti[s2]

            #print_problems_settings(shipper1, shipper2)

            z1 = cost1          # sum(cost for cost in shipper1[3])
            z2 = cost2          # sum(cost for cost in shipper2[3])

            print("Solution values after cooperation (" + str(steps) + " steps):")

            if i%2==0:
                writer.writerow({'step': str(steps), 'nor1': str(len(route1)), 'nor2': str(len(route2)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.', ','),
                                 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z1).replace('.', ','),
                                 'z2': str(z2).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','),
                                 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','),
                                 'ez1': str(ub_s2).replace('.', ','), 'ez2': str(lb_s1).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
            else:
                writer.writerow({'step': str(steps), 'nor1': str(len(route2)), 'nor2': str(len(route1)),
                                 'nos': str(len(customers_to_move)), 'saving': str(total_saving_s1).replace('.', ','),
                                 'delta': str(total_additional_cost_s2).replace('.', ','),
                                 'gain': str(total_saving_s1 - total_additional_cost_s2).replace('.', ','),
                                 'z1': str(z2).replace('.', ','),
                                 'z2': str(z1).replace('.', ','), 'ztot': str(z1 + z2).replace('.', ','),
                                 'zgain': str(old_z1 + old_z2 - z1 - z2).replace('.', ','),
                                 'ez1': str(lb_s1).replace('.', ','), 'ez2': str(ub_s2).replace('.', ','),
                                 'eztot': str(lb_s1 + ub_s2).replace('.', ',')})
        else:
            print("Solution values after cooperation (" + str(i) + " steps):")

        s1opt = 0
        s2opt = 0

        if s1 == 0:
            print("S1 optimal cost --> " + str(z1))
            print("S2 optimal cost --> " + str(z2))
            s1opt = z1
            s2opt = z2
        else:
            print("S1 optimal cost --> " + str(z2))
            print("S2 optimal cost --> " + str(z1))
            s2opt = z1
            s1opt = z2

        print("Sum of costs --> " + str(z1 + z2))

        print("Cooperation gain --> " + str((s1_sol + s2_sol) - (z1 + z2)))

        print(route1, route2, s1opt, s2opt)
        return route1, route2, s1opt, s2opt

#main()
#
#