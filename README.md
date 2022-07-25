# A Cooperative Vehicle Routing Platform for Logistic Management

The platform implements a cooperative routing algorithm for the transport of goods initially presented in [1].
With the help of some colleagues working in the field of biomedical research and healtcare I have also adapted the platform to the healthcare context to allow the cooperation between two independent healthcare organizations (shippers) that manage their own vehicle fleets in a given geographic area in order to obtatin a reduction in distribution logistic costs.
See [2] for more details.

[1] Manlio Gaudioso, Giovanni Giallombardo, and Giovanna Miglionico. 2018. A savings-based model for two-shipper cooperative routing. (01 2018).

[2] Valentina Falvo, Mariagrazia Scalise, Francesco Lupia, Pierfrancesco Casella, Mario Cannataro. 2018. A Cooperative Vehicle Routing Platform for Logistic Management in Healthcare. BCB 2018: 689-692

## About the platform

The functional components were implemented using the Python language. In particular, the prototype was implemented in a Web Application using the popular Django framework based on the Python language.
Behind the scenes, the prototype adopts, among the various options initially considered, the open source toolkit JSPRIT, developed by Stefan Schröder, to solve the complex problems of Vehicle Routing (VRP); note that this solver is made available in the form of a Java library, for which appropriate functions have been developed to allow the interoperability of this library with the rest of the Python prototype.
As for the interaction with the user, the Web Application uses the Javascript language and the jQuery library and makes use of the Bootstrap library for the implementation of the graphic components that allow the user to interact with all the features of the prototype created.
Finally, the technology uses the Mapbox framework to draw and visualize the routes and for the representation of the input and output data uses JSON and XML respectively.

## Installation
Simply execute `docker-compose up --build`

## Usage
Navigate to http://localhost:8000 

## Disclaimer
This software is for research purpose only. Do not use in production.

