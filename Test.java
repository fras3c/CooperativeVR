
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


                int vehiclesNumber = 2;
                int capacity = 50;

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
                
VehicleRoutingTransportCostsMatrix.Builder costMatrixBuilder = VehicleRoutingTransportCostsMatrix.Builder.newInstance(true);costMatrixBuilder.addTransportDistance("0", "1", 105.6492);
costMatrixBuilder.addTransportDistance("0", "2", 42.9288);
costMatrixBuilder.addTransportDistance("0", "3", 74.58510000000001);
costMatrixBuilder.addTransportDistance("0", "4", 123.4685);
costMatrixBuilder.addTransportDistance("1", "2", 66.0907);
costMatrixBuilder.addTransportDistance("1", "3", 128.8029);
costMatrixBuilder.addTransportDistance("1", "4", 42.4909);
costMatrixBuilder.addTransportDistance("2", "3", 21.8545);
costMatrixBuilder.addTransportDistance("2", "4", 60.8988);
costMatrixBuilder.addTransportDistance("3", "4", 88.6333);


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

            for(int i=1; i <=4; i++){
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
        