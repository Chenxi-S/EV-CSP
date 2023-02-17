# EV-CSP

This is the code repository for the paper "A Data-Driven Approach for Optimizing Early-Stage Electric Vehicle Charging Station Placement" in Transactions on Industrial Informatics.

### Reference 
C. Sun, T. Li and X. Tang, ["A Data-Driven Approach for Optimizing Early-Stage Electric Vehicle Charging Station Placement,"](https://ieeexplore.ieee.org/document/10045802) in IEEE Transactions on Industrial Informatics, doi: 10.1109/TII.2023.3245633.
For any questions, you may contact sunchenxi AT cuhk DOT edu DOT cn.

### data
The POI data and the population data for the city of Haikou are provided. 
* The population data is from [Worldpop](https://www.worldpop.org).
* The trajectory data was from [DIDI GAIA Initiative](https://gaia.didichuxing.com), which was no longer publicly available since 2022. Due to the permissions requirements, we cannot provide the data together with the implementation. 

### code 
Due to data permission requirements, we provide the implementation of the proposed approach for two settings (delta-nearest model and K-nearest model) using only population data. 


### Requirement 
* numpy
* pandas


