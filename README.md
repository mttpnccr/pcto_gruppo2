# Project Status
The project is in the alpha test status.
# Title

Project Work #1
The application must be able to answer to three different types of question.

>In the first one, it must provide the overall length and duration in minutes of a trip, knowing source and destination.

>In the second task, the application must provide the same information as the first question but comparing four different departure time.

>In the last one, the application must find the closest specified place from the type of place and the source address.

# Index

- [How to start](#how-to-start)
- [How to contribute](#how-to-contribute)
- [Maintenance and Licensing](#maintenance-licensing-authors-and-copyright)

# How to start
### How to install
You needn't to install nothing. You only need your browser because all the work is on Internet. You should create your personal account on [AWS](https://developer.amazon.com/alexa/console/ask) (Amazon Web Services) and on Alexa developer console. Now you could create your lambda function using services like API Gateway, Lambda or CloudWatch and an esternal service called [Postman](https://www.postman.com/). While in the Alexa developer console side you can create your personal skill and link them to your Lambda Function using the API gateway.

### Documentation
#### Link to external documentation
*Google Maps API documentation: [Getting directions through the Directions API](https://developers.google.com/maps/documentation/directions/get-directions?hl=it#TravelModes)*
*Google Maps API documentation: [Find Place](https://developers.google.com/maps/documentation/places/web-service/search-find-place?hl=it)*
*Python w3school3: [Lessons](https://www.w3schools.com/python/)*

# How to contribute
You can contribute with this project only by supporting me and giving me useful advice for its improvement.

## Project Structure
There are three main directories in this project. The firts one contains files and programs concerning the management of Alexa. The other two are about the two Lambda Function. One is for the first two tasks (maps) while for the last task there is the findplace directory.

## Bug reports and requests for help
A bug was found in the creation of the FindPlace intent creating the expression examples. When we used the basic example with only source and destination, and assigning these two attributes the type Street Name, the second parameter was ignored and not registered in the slots unless there was some other attributes after it. It's for this reason that in the application there is no simple request with only source and destination specified. Can you tell me the reason for this problem?

# Maintenance, Licensing, Authors and Copyright
Giuliano Antonenko and Matteo Panicciari

## Licenze software dei componenti di terze parti
*Alexa Developer Console: [Alexa](https://developer.amazon.com/alexa/console/ask)*
