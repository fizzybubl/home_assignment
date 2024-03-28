# Selenium Interface
A custom implementation on top of selenium webdriver/webelement, that aims
to improve page/element traversing by adding custom waiters.

# Design choices
## WebDriver/WebElement extension

Extension is done through inheritance, to add new functionality and keep the old
one at the same time.


## Page objects

There are several ways of implementing the page objects:
1. From a responsibility point of view, we can implement
   1. A general class, that contains all the logic for navigating a website.
   2. Specialized classes, that know how to traverse only a set of pages(eg: a landing page).
   3. Specialized HTML components classes, that know how to traverse only certain parts of a landing page.

2. From a loading point of view, we can:
   1. Implement eager loading, auto scrapping pages, that load a set of given attributes
   on object instantiation.
   2. Implement lazy loading, auto scrapping pages, that load a set of given attributes
   on attribute access.
   3. Implement manual scrapping pages, which scrape the data which is specified by calling
   specific methods.


## Throttle actions
In order to throttle actions per minute (clicks, inputs), time sleeps should be implemented
for each click/write method. This should be done in a way that does not alter the 
implementation of the custom web driver, but overrides and extends the behaviour
by adding parametrized sleep time.

Parametrized sleep time can be at:
* function level - through a function parameter
* class level - through a configurable class attribute
* module level - through a module constant
* package level - through a package constant, which is configurable


