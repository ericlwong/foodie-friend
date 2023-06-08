# FoodieFriend - Hackbright Final Project

## Overview
FoodieFriend is a full-stack web application that will allow users to search for and view restaurants surrounding a location of their choice by interfacing with Yelp's Fusion API. Via Yelp, users will be able to view details of individual restaurants, including rating and up to three images and reviews. For convencience, users may favorite individual restaurants to a personal list to revisit at a later time or to keep track of restaurants they enjoy. Furthermore, FoodieFriend implements both Google's Maps and Directions API's to display restaurant locations and allow users to retrieve directions to any particular restaurant with routes curated by various travel modes available.

## Technology Stack
Python, Flask, Jinja2, PostgreSQL, SQL Alchemy, HTML, CSS, JavaScript, Bootstrap

## APIs
- Yelp Fusion
- Google Maps
- Google Directions

## Data Model
For those interested in viewing how FoodieFriend's data has been modeled: https://dbdiagram.io/d/6457628cdca9fb07c4a3bfd9

## Core Features

### Search for restaurants
![alt text](https://github.com/ericlwong/foodie-friend/blob/main/static/images/screenshots/homepage-screen.png "Homepage")
Upon visiting FoodieFriend, the user is greeted with a large input group in which they must provide a search term in addition to a defined location. If logged in, the location input field will be prefilled with the user's city and state they inputted during registration. For the search term input, the user may enter a specific restaurant name or a particular food/cuisine category. Once the user hits the search icon, FoodieFriend will begin its search by first querying its database for any matching records to meet a minimum length of ten restaurants. If less than ten have been found, FoodieFriend will then call Yelp's Fusion API to pull additional restaurants matching the search term and store them into the database for faster searches in the future.

### Viewing search results
Once the search is complete, FoodieFriend will display a number of restaurants matched or are similar to the search term and location the user inputted on the homepage in a flushed list. Accompanying the list of restaurants is a map where each restaurant listing is rendered as a marker on it through the implementation of the Google Maps API. The user may click on any marker to view information about the restaurant, such as its rating, address, and phone number. To improve the user experience in scenarios where the map may have many markers clustered together, each marker has a bouncing animation set to trigger if the user hovers over its respective restaurant in the list. In addition, hovering over any marker will highlight its respective restaurant in the list. The user may view the details of a particular restaurant by clicking it in the list or clicking the restaurant name within its map marker info window.

### Viewing a particular restaurant
The user will be able to view important information in regards to a restaurant. They will be able to take a look at the rating, address, phone number, business hours, and up to three images and reviews provided by Yelp's Fusion API. In addition to Yelp reviews, users of FoodieFriend may also write their own reviews for the restaurant. To help distinguish between the two types of reviews, all Yelp reviews have a red Yelp icon in the lower left corner of their containers. The user may write their own review where they must provide an appropriate rating and review body. As the user has the ability to write a review, they also can delete it via a delete button that only exists within a review they wrote. In addition to writing a review, the user may also favorite the restaurant. Favoriting the restaurant allows the user to save it to a personal list, viewable within their profile dashboard. Finally, the user may get directions to the restaurant via the "Get Directions" button or the map icon next to the address.

### Getting directions to a restaurant
The restaurant's address is pre-filled and set to read-only to ensure the directions will always be routed to or from the restaurant without error. The user has the ability to input the starting or ending address depending on whether they are trying to route to or from the restaurant. In addition, the user may select from four travel modes: Driving, Transit, Bicycling, and Walking. Depending on the travel mode selected, the map will render the best suited route. When the user hits the "Get directions" button, not only will a visual route be generated on the map, but directions in text will display under the form inputs as well.

### Personal lists
Within the user's profile page, the user will be able to create any number of lists to favorite, or save, restaurants to for viewing at a later time. As restaurants are favorited, they will appear as new list items within each list container as clickable references to their respective details pages. Furthermore, each restaurant within the list will have an accompanying delete button in the form of a trashcan icon next to them. Within each list container, there will be a delete button at the bottom. Both delete actions will trigger a pop-up modal for the user to confirm whether they indeed want to go through with the delete action. Confirming the delete actions will remove the respective item as such.