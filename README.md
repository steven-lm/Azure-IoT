## Overview

A python script which monitors COVID-19 cases in NSW by scraping multiple websites. Data is sent to Azure IoT hub, processed with Stream Analytics and visualised using Power BI.


## Table of contents
* [IoT Hub](#iot-hub)
* [Stream Analytics](#stream-analytics)
* [Setup & Dependencies](#setup)

## IoT Hub
Formatting: JSON

Data:
  - Total cases
  - Active cases
  - AU Cases
  - NSW Cases
  - NSW Active cases
  - News updates

## Stream Analytics
Input : IoT Hub
Output: PowerBI

## Setup
-Chromedriver installed in '/chrome/chromedriver' path
