import os.path, subprocess
from subprocess import STDOUT,PIPE
from subprocess import check_output
import numpy
import requests
import json
import xml.etree.ElementTree as ET

def BuildCode(nrVehicles, capacity, nrClients, costMatrix):

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
    public class Test {

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
                VehicleRoutingTransportCostsMatrix.Builder costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(true);
                costMatrixBuilder.addTransportDistance("0", "1", 15.0);
                costMatrixBuilder.addTransportDistance("0", "2", 5.0);
                costMatrixBuilder.addTransportDistance("0", "3", 9.0);
                costMatrixBuilder.addTransportDistance("1", "2", 3.0);
                costMatrixBuilder.addTransportDistance("1", "3", 2.0);
                costMatrixBuilder.addTransportDistance("2", "3", 20.0);
                */

                /*
                 * build services at the required locations, each with a capacity-demand of 1.
                 */
  //               Service service1 = Service.Builder.newInstance("A").addSizeDimension(WEIGHT_INDEX, 7).setLocation(Location.newInstance(1)).build();
    //            Service service2 = Service.Builder.newInstance("B").addSizeDimension(WEIGHT_INDEX, 3).setLocation(Location.newInstance(2)).build();
   //             Service service3 = Service.Builder.newInstance("C").addSizeDimension(WEIGHT_INDEX, 8).setLocation(Location.newInstance(3)).build();
    //	        Service service4 = Service.Builder.newInstance("D").addSizeDimension(WEIGHT_INDEX, 2).setLocation(Location.newInstance(37, 70)).build();
    //
    //	        Service service5 = Service.Builder.newInstance("E").addSizeDimension(WEIGHT_INDEX, 6).setLocation(Location.newInstance(70, 12)).build();
    //	        Service service6 = Service.Builder.newInstance("F").addSizeDimension(WEIGHT_INDEX, 3).setLocation(Location.newInstance(80, 44)).build();
    //	        Service service7 = Service.Builder.newInstance("G").addSizeDimension(WEIGHT_INDEX, 7).setLocation(Location.newInstance(90, 70)).build();
    //	        Service service8 = Service.Builder.newInstance("H").addSizeDimension(WEIGHT_INDEX, 5).setLocation(Location.newInstance(98, 14)).build();
    //
    //	        Service service9 = Service.Builder.newInstance("I").addSizeDimension(WEIGHT_INDEX, 6).setLocation(Location.newInstance(76, 15)).build();
    //	        Service service10 = Service.Builder.newInstance("J").addSizeDimension(WEIGHT_INDEX, 4).setLocation(Location.newInstance(79, 50)).build();
    //	        Service service11 = Service.Builder.newInstance("K").addSizeDimension(WEIGHT_INDEX, 8).setLocation(Location.newInstance(40, 80)).build();
    //	        Service service12 = Service.Builder.newInstance("L").addSizeDimension(WEIGHT_INDEX, 6).setLocation(Location.newInstance(38, 77)).build();
    //


   //             vrpBuilder.addJob(service1).addJob(service2).addJob(service3);
    //	        .addJob(service4).
    //	        addJob(service5).addJob(service6).addJob(service7).addJob(service8).
    //	        addJob(service9).addJob(service10).addJob(service11).addJob(service12);

            for(int i=1; i <='''+str(nrClients)+'''; i++){
                Service s = Service.Builder.newInstance(""+i).addSizeDimension(WEIGHT_INDEX, 3).setLocation(Location.newInstance(i)).build();
                vrpBuilder.addJob(s);
            }

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

                /*
                 * plot
                 */
                //new Plotter(problem,bestSolution).plot("output/plot.png","simple example");

                /*
                render problem and solution with GraphStream
                 */
               // new GraphStreamViewer(problem, bestSolution).labelWith(Label.ID).setRenderDelay(200).display();
            }

        }
        '''
    with open('Test.java', 'w') as the_file:
        the_file.write(code)

def compile_java(java_file):
    subprocess.check_call(['javac', '-cp', '.:/Users/flupia/Documents/workspace/NextShop5_2/lib/*', java_file])

def execute_java(java_file):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', '-cp', '.:/Users/flupia/Documents/workspace/NextShop5_2/lib/*', java_class]
    #proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='utf8')
    try:
        ans = check_output(['java', '-cp', '.:/Users/flupia/Documents/workspace/NextShop5_2/lib/*', java_class])
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    #stdout,stderr = proc.communicate(stdin)
    solution = ans.decode("utf8")
    print(solution)

    if "solution" in solution:
        route,costs=parseXML("output/problem-with-solution.xml")
        print(route)
        print(costs)
    return route, costs

    #print ('This was "' + stdout + '"')

def BuildCostMatrix(A):

    costMatrix = '''VehicleRoutingTransportCostsMatrix.Builder costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(true);'''

    for i in range(len(A)):
        for j in range(len(A[0])):
            if i < j:
                costMatrix += '''costMatrixBuilder.addTransportDistance("'''+str(i)+'''", "'''+str(j)+'''", '''+str(A[i][j])+''');'''+"\n"

    print(costMatrix)

    return costMatrix

def GenerateCoordinates(nrClients):
    N = 39.33
    S = 38.9669
    O = 16.31
    E = 16.98

    lats = numpy.random.uniform(S, N, size=nrClients)
    lons = numpy.random.uniform(O, E, size=nrClients)
    lats = numpy.append([38.926], lats)
    lons = numpy.append([16.4857], lons)
    print(f"Coordinate deposito: {lats[0]}, {lons[0]}")

    A = [ [0 for i in range(len(lats))] for j in range(len(lats)) ]

    params = (('access_token', 'pk.eyJ1IjoiaWN0c3VkIiwiYSI6ImNqdjJmbmR5ZjA0YW80ZW5taG1yaDFxcmgifQ.N2ggfxhBwmp2woNno3X7CQ'),)

    for i in range(len(lats)-1):
        print(f"({lats[i+1]},{lons[i+1]})")
        for j in range(i+1, len(lats)):
            response = requests.get(f"https://api.mapbox.com/optimized-trips/v1/mapbox/driving/{lons[i]},{lats[i]};{lons[j]},{lats[j]}", params=params)
            json_data = json.loads(response.text)
            #distance = float(json_data['trips'][0]['distance'])
            distance = float(json_data['trips'][0]['legs'][0]['distance'])

            A[i][j] = distance*0.001

    printMatrix(A)
    return lats, lons, A



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
        return routes2,cost



def run(nrClients):
    lat,lon = 38.926, 16.4857

    NrVehicles = 2
    capacity = 50
    #nrClients = 10

    print("Coordinate consegne:")
    lats, lons, A = GenerateCoordinates(nrClients)
    '''
    A= [[0, 15, 5, 9],
         [15, 0, 3, 2],
         [5, 3, 0, 20],
         [9, 2, 20, 0]
        ]
    '''
    costMatrix = BuildCostMatrix(A)

    BuildCode(NrVehicles, capacity, nrClients, costMatrix)

    compile_java('Test.java')
    route, costs = execute_java('Test.java')
    return lats, lons, route, costs

#run()

