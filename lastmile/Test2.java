
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
    public class Test2 {

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


                int vehiclesNumber = 2;
                int capacity = 100;

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

                
				vrpBuilder.addJob(Service.Builder.newInstance("3").addSizeDimension(WEIGHT_INDEX, 1).setLocation(Location.newInstance("3")).build());
				vrpBuilder.addJob(Service.Builder.newInstance("4").addSizeDimension(WEIGHT_INDEX, 1).setLocation(Location.newInstance("4")).build());
				vrpBuilder.addJob(Service.Builder.newInstance("5").addSizeDimension(WEIGHT_INDEX, 1).setLocation(Location.newInstance("5")).build());
				vrpBuilder.addJob(Service.Builder.newInstance("2").addSizeDimension(WEIGHT_INDEX, 1).setLocation(Location.newInstance("2")).build());



                /*
                 * build services at the required locations, each with a capacity-demand of 1.
                 */

            
				VehicleRoutingTransportCostsMatrix.Builder costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(true);
				costMatrixBuilder.addTransportDistance("0", "3", 123.5528);
				costMatrixBuilder.addTransportDistance("0", "4", 27.029200000000003);
				costMatrixBuilder.addTransportDistance("0", "5", 68.52510000000001);
				costMatrixBuilder.addTransportDistance("0", "2", 60.73780000000001);
				costMatrixBuilder.addTransportDistance("3", "4", 62.3287);
				costMatrixBuilder.addTransportDistance("3", "5", 69.4472);
				costMatrixBuilder.addTransportDistance("4", "5", 95.33200000000001);
				costMatrixBuilder.addTransportDistance("2", "3", 45.572900000000004);
				costMatrixBuilder.addTransportDistance("2", "4", 30.7975);
				costMatrixBuilder.addTransportDistance("2", "5", 40.567099999999996);



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
        