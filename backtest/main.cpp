#include <stdio.h>
#include <string>
#include <fstream>
#include <vector>
#include <iostream> 
#include <utility> // std::pair
#include <stdexcept> // std::runtime_error
#include <sstream> // std::stringstream

#include "SoCKalman.h"


std::string NODE_FILEPATH = "../data/node_data.csv";
std::string INPUT_FILEPATH = "../data/raw_sensor_data.csv";
std::string OUTPUT_FILEPATH = "../data/processed_sensor_data.csv";


void write_csv(std::string filename, std::vector<std::pair<std::string, std::vector<int> > > dataset){
    // Make a CSV file with one or more columns of integer values
    // Each column of data is represented by the pair <column name, column data>
    //   as std::pair<std::string, std::vector<int>>
    // The dataset is represented as a vector of these columns
    // Note that all columns should be the same size
    
    // Create an output filestream object
    std::ofstream myFile(filename);
    
    // Send column names to the stream
    for(int j = 0; j < dataset.size(); ++j)
    {
        myFile << dataset.at(j).first;
        if(j != dataset.size() - 1) myFile << ","; // No comma at end of line
    }
    myFile << "\n";
    
    // Send data to the stream
    for(int i = 0; i < dataset.at(0).second.size(); ++i)
    {
        for(int j = 0; j < dataset.size(); ++j)
        {
            myFile << dataset.at(j).second.at(i);
            if(j != dataset.size() - 1) myFile << ","; // No comma at end of line
        }
        myFile << "\n";
    }
    
    // Close the file
    myFile.close();
}

std::pair<int, int> read_node_data(std::string filename){

    // Create pair to store the result
    std::pair<int, int> result;

    // Create an input filestream
    std::ifstream myFile(filename);

    // Make sure the file is open
    if(!myFile.is_open()) throw std::runtime_error("Could not open file");

    // Declare helper vars
    std::string line, colname;
    int val;
    if(myFile.good())
    {
        // Extract the first line in the file
        std::getline(myFile, line);

        // Skip and extract the second line in the file to get the values
        std::getline(myFile, line);
  

        // Create a stringstream from the line
        std::stringstream ss(line);
 
        // Keep track of colIdx
        int colIdx = 0;

        // Extract each integer
        while(ss >> val){
            // Add the current integer to the result pair

            if (colIdx == 0) {
                result.first = val;
            } else {
                result.second = val;
            }

            // If the next token is a comma, ignore it and move on
            if(ss.peek() == ',') ss.ignore();

            colIdx ++;
            

        }
        
        return result;
    }

}

std::vector<std::pair<std::string, std::vector<int> > > process_csv(std::string filename){
    // Reads a CSV file into a vector of <string, vector<int>> pairs where
    // each pair represents <column name, column values>

    // Instantiate kalman filter and initialize values
    SoCKalman kalman;

    // Get node battery type and voltage
    std::pair<int, int> batteryInfo = read_node_data(NODE_FILEPATH);

    bool isBatteryLithium = (bool)batteryInfo.first;
    bool isBattery12V = (batteryInfo.second == 12) ? true : false;
    
    float batteryEff = 85000;
    float initialSoC = 0xFFFFFFFF;
    float batteryCapacityAh = 12; //default 1200Wh. now 12Ah*12V=144Wh, emblem 17Ah  
    printf("Parameter set: \n BatteryEfficiency: %f\n",batteryEff);
    printf(" IntialSoC: %f\n",initialSoC);
    printf(" batteryCapacityAh: %f\n",batteryCapacityAh);
    printf(" isBatteryLithium?: %f\n",isBatteryLithium);
    printf(" isBattery12V?: %f\n\n",isBattery12V);
    
    // Create a vector of <string, int vector> pairs to store the result
    std::vector<std::pair<std::string, std::vector<int> > > result;

    // Create an input filestream
    std::ifstream myFile(filename);

    // Make sure the file is open
    if(!myFile.is_open()) throw std::runtime_error("Could not open file");

    // Helper vars
    std::string line, colname;
    float val;

    // Read the column names
    if(myFile.good())
    {
        // Extract the first line in the file
        std::getline(myFile, line);

        // Create a stringstream from line
        std::stringstream ss(line);

        // Extract each column name
        while(std::getline(ss, colname, ',')){

            if (colname == std::string("timestamp")) {
                break;
            }

            // Initialize and add <colname, int vector> pairs to result
            std::pair<std::string, std::vector<int> > column;
            column.first = colname;
            result.push_back(column);
        }
        // Add new column for Kalman SoC
        std::pair<std::string, std::vector<int> > column;
        std::string colname("kalman_soc");
        column.first = colname;
        result.push_back(column);
    }


    int lineIdx = 0;
    // Read data, line by line
    while(std::getline(myFile, line))
    {
        // Create a stringstream of the current line
        std::stringstream ss(line);
        
        // Keep track of the current column index
        int colIdx = 0;
        
        // Extract each integer
        while(ss >> val){
            if (colIdx == 5) {
                break;
            }
            // Add the current integer to the 'colIdx' column's values vector
            result.at(colIdx).second.push_back(val);
            // If the next token is a comma, ignore it and move on
            if(ss.peek() == ',') ss.ignore();
            
            // Increment the column index
            colIdx++;
        }
        if (lineIdx == 0) {
            // use battery voltage to initialize kalman filter
            float batteryVoltage = result.at(3).second.back();
            printf("Parameter the EKF is init: \n BatteryEfficiey: %f\n",batteryEff);
            printf(" IntialSoC: %f\n",initialSoC);
            printf(" batteryCapacityAh: %f\n",batteryCapacityAh);
            printf(" isBatteryLithium?: %f\n",isBatteryLithium);
            printf(" isBattery12V?: %f\n",isBattery12V);
            printf(" BatteryVoltage in mV: %f\n\n",batteryVoltage);
            kalman.init(isBattery12V, isBatteryLithium, batteryEff, batteryVoltage, initialSoC);
            float soc = kalman.read();
            printf("Effiency calcultated by EKF init %f\n\n",kalman.efficiency());
            printf("The SoC Caculated by EKF init: %f\n\n",soc);
            result.at(colIdx).second.push_back(soc);
        } else {
            // use sensor data to do a sample with the kalman filter
            printf("\n\nTimeStep: %d\n\n",lineIdx+2);
            bool isBatteryInFloat = (result.at(2).second.back() == 3);
            float batteryMilliAmps = result.at(0).second.back();
            float batteryVoltage = result.at(3).second.back();
            float batteryMilliWatts = result.at(1).second.back();
            float samplePeriodMilliSec = result.at(4).second.back();
            kalman.sample(isBatteryInFloat, batteryMilliAmps, batteryVoltage, batteryMilliWatts, samplePeriodMilliSec, batteryCapacityAh);
            float soc = kalman.read();
            result.at(colIdx).second.push_back(soc);
        }
        lineIdx++;
    }

    // Close file: %B\n",isBatteryLithium
    myFile.close();

    return result;
}

int main() {

    // Read and process sensor data using kalman filter
    std::vector<std::pair<std::string, std::vector<int> > > result = process_csv(INPUT_FILEPATH);

    printf("Finished reading.\n");

    // Write to another file to check that this was successful
    write_csv(OUTPUT_FILEPATH, result);

    printf("Finished writing.\n");  
    
    return 0;
}