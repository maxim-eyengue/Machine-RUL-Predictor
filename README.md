![Illustration]("images/hydraulic_cylender.png")

# Machine-RUL-Predictor
An application designed to predict the remaining useful life of critical components in construction machinery by using machine data.

# Problem description

The goal of this project is to **predict the Remaining Useful Life (RUL)** of components of a machine  by analyzing **IoT** and **operations data**. This can be useful for predictive maintenance tasks where we decide on the maintenance to perform on asset data depending on what is the most critical. For example, we can prioritize components with the lower remaining useful life.

<h3>Machine RUL Dataset</h3>

<p>The <a href="https://www.kaggle.com/datasets/sasakitetsuya/machine-rul-data">dataset</a> was created to simulate data related to the predictive maintenance of critical components in construction machinery, such as cranes, excavators, and bulldozers. It contains 1,000 records, each representing a unique component.

</p>

<h3>Features Description:</h3>
<ul>
    <li><strong>Component_ID</strong>: A unique identifier for each component, formatted as CMP0001 to CMP1000 [Text]</li>
    <li><strong>Component_Type</strong>: The type of component [Engine, Hydraulic Cylinder, Gear]</li>
    <li><strong>Vibration</strong>: The vibration level of the component, measured between 0.1 and 5.0
        [Numeric: arbitrary units ]</li>
    <li><strong>Temperature</strong>: The operating temperature of the component, ranging from 40 to 100
        [Numeric: degrees Celsius]</li>
    <li><strong>Pressure</strong>: The pressure exerted on the component, ranging from 50 to 300. [Numeric: psi]</li>
    <li><strong>Operating_Hours</strong>: The total time the component has been in operation, ranging from 0 to 5,000.
        [Numeric: hours]</li>
    <li><strong>Remaining_Useful_Life (RUL)</strong>: The estimated time left before the component fails, randomly assigned within a range of 50 to 1,000.
        [Numeric: hours]</li>
</ul>

### **Disclaimer** 🛑  
The dataset used in this project is **synthetic** and has been generated rather than collected from real-world sources. ⚠️ Due to the lack of transparency in the data synthesis process, the exact methods and criteria used are **unknown** 🤷‍♂️. As a result, the patterns and relationships within the data may not accurately reflect real-world phenomena 🌍. 

### Project plan
Detailed instructions have been provided [here](./plan.md).