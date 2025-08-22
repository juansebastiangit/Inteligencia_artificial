# PIRIS Model with Bayesian Hyperparameter Optimization

This repository contains a Kaggle notebook that implements the PIRIS (Physics Informed Relevant Information Simulation) model for simulating ion adsorption onto various nanomaterial surfaces. The project leverages Bayesian Optimization via the Optuna framework to efficiently tune the simulation's hyperparameters, achieving optimal results with minimal manual intervention.

The entire simulation pipeline—from sample generation to final analysis—is automated and configured to save all resulting visualizations and artifacts directly to this GitHub repository.

## Key Features

-   **Modular Sample Generation:** Functions to procedurally generate three distinct atomic structures:
    1.  A 2D graphene-like ZnO sheet.
    2.  A 3D spherical Aluminum (Al) nanoparticle with an FCC lattice.
    3.  A 3D armchair ZnO nanotube.
-   **Bayesian Hyperparameter Tuning:** Utilizes Optuna with a Gaussian Process sampler to intelligently search for the optimal set of hyperparameters, including PRI regularization weights, learning rate, and initial ion distance.
-   **TensorFlow-Powered Simulation:** The core energy calculations and gradient-based optimization are implemented in TensorFlow for high performance, especially on GPU accelerators.
-   **Automated Visualization:** Automatically generates and saves key plots for analysis:
    -   Hyperparameter importance plots.
    -   Contour plots for hyperparameter interactions.
    -   3D visualizations of initial and final system states.
    -   Loss evolution curves during training.
-   **Performance Scaling Analysis:** Includes a dedicated section to analyze the computational scaling of the PIRIS model with respect to the number of atoms in the system, comparing it against theoretical DFT scaling laws.
-   **Integrated Git Workflow:** Seamlessly commits and pushes all generated artifacts from the Kaggle notebook environment to this GitHub repository at the end of each run.

## Methodology

The simulation pipeline follows a structured, multi-stage process for each sample:

### 1. Initial State Generation
Before optimization, a set of diverse starting positions for the ion adsorption is required. This is achieved by:
-   Calculating the spatial boundaries of the target nanomaterial.
-   Generating a dense grid of candidate points (for planar structures) or direction vectors (for 3D structures) within these boundaries.
-   Using the **k-means++** algorithm to select a `k` number of well-distributed starting configurations from the candidates. This ensures the optimization process explores a varied set of initial conditions.

### 2. Bayesian Optimization
For each of the `k` starting configurations, an Optuna study is performed to find the best hyperparameters.
-   **Objective:** To minimize the final physical energy of the system after a condensed training run.
-   **Hyperparameters Tuned:**
    -   `factor`: The initial distance of the ion from the surface, scaled by a characteristic length.
    -   `pri_weight`, `lambda_pri`, `sigma_pri`: Parameters governing the Priciple of Relevant Information (PRI) regularization therm.
    -   `learning_rate`, `decay_rate`: Parameters for the Adam optimizer's learning schedule.
-   **Sampler:** A Gaussian Process (GP) sampler is used, which is highly effective for continuous parameter spaces.

### 3. Final Training
Once the best set of hyperparameters and the corresponding initial configuration are identified, a full, longer training run is executed. This simulation uses the optimal parameters to find the lowest-energy final position for the ion(s).

### 4. Evaluation and Visualization
After the final training, the system is evaluated. The notebook generates a summary of the physical results (e.g., total energy, adsorption energy per ion) and produces the full suite of visualizations, which are saved as PDF files.

## Notebook Structure

The `piris-bo.ipynb` notebook is organized into the following sections:

1.  **Libraries and Setup:** Installs dependencies and imports all necessary libraries.
2.  **Simulation Core Functions:** Defines all reusable functions for the pipeline.
    -   *K-Means++ for Initial Position Generation*
    -   *Ion Placement and Adsorption Setup*
    -   *Loss Function Definition*
    -   *Training Utilities*
3.  **Bayesian Optimization Workflow:** Contains the Optuna objective function and the main optimization loop.
4.  **Final Model Training:** Defines the final training loop that uses the optimized hyperparameters.
5.  **Final Evaluation and Results:** Defines functions to calculate final metrics and generate plots.
6.  **Simulation Runs:** Executes the entire pipeline for each of the three sample materials.
7.  **Performance Scaling Analysis:** Runs the simulation on increasingly large samples to measure and plot computational complexity.
8.  **Push Results to GitHub:** Commits and pushes all saved artifacts to the repository.

## How to Run This Project

This project is designed to be run in a Kaggle Notebook environment.

### Prerequisites
-   A [GitHub](https://github.com/) account.
-   A [Kaggle](https://www.kaggle.com/) account.

### Setup Steps
1.  **Fork this Repository:** Fork this project to your own GitHub account.

2.  **Create a GitHub Personal Access Token (PAT):**
    -   Go to your GitHub **Settings -> Developer settings -> Personal access tokens -> Tokens (classic)**.
    -   Generate a new token.
    -   Give it a descriptive name (e.g., `kaggle-notebook-access`).
    -   Set an expiration date.
    -   Select the `repo` scope. This is required to allow the notebook to push files to your repository.
    -   **Copy the generated token immediately.** You will not be able to see it again.

3.  **Set up Kaggle Secrets:**
    -   Create a new Kaggle Notebook and upload the `PIRIS.ipynb` file from this repository (**File -> Upload notebook**).
    -   In the notebook editor, go to the **Add-ons -> Secrets** menu.
    -   Click **"Add a new secret"**.
    -   Enter `GITHUB_PAT` as the label (the key).
    -   Paste your GitHub PAT as the value.

4.  **Configure the Kaggle Environment:**
    -   Make sure to change the GITHUB_USER variable to your username.
    -   In the notebook settings panel (on the right), ensure that **Internet is turned ON**.
    -   For best performance, enable a **GPU accelerator** (e.g., T4 x2).

### Execution
With the setup complete, you can run the entire notebook by clicking **"Run All"**. The notebook will execute all simulations, generate plots, and push them to your forked repository.

## Adding Custom Samples
The simulation pipeline is designed to be modular, allowing for easy integration of new nanomaterial samples. To add your own custom structure, follow these steps:

### 1. Create a Sample Generation Function
Create a new Python function that generates the atomic coordinates for your sample. It's recommended to use one of the existing functions (e.g., `muestra_Al_dummy`) as a template.

The most important requirement is that your function **must** return the following six values in the correct order and format:

-   `num_atoms` (`int`): The total number of atoms in the structure.
-   `positions` (`np.ndarray`): A NumPy array of shape `(N, 3)` containing the (x, y, z) coordinates of each atom.
-   `elements` (`np.ndarray`): A NumPy array of shape `(N,)` containing the string label for each atom (e.g., `"Al"`, `"Zn"`).
-   `sample_atoms` (`tf.Tensor`): The `positions` array converted to a `tf.float32` tensor.
-   `sample_elements` (`tf.Tensor`): The `elements` array converted to a `tf.string` tensor.
-   `geometria` (`str`): A crucial string that must be either `"planar"` or `"3D"`. This determines how the simulation calculates boundaries for ion placement.

### 2. Define Simulation Parameters
In a new cell, create the `params` and `param_tensors` dictionaries specific to your new material. This involves defining the `atom_types`, the `ion_type` to be adsorbed, and their physical properties (sigma, epsilon, charge) in the `atom_params` sub-dictionary. You can copy the boilerplate code that builds `param_tensors` from `params`.

### 3. Add an Execution Cell
Copy an existing execution block (e.g., the one for "Sample 1") and modify it:
-   Update the `sample_name` variable to a unique name for your new sample. This will be used for naming the output plot files.
-   Call your new sample generation function.
-   Ensure the main pipeline functions (`optimization`, `training_loop`, etc.) are called with your new `params` and `param_tensors` dictionaries.

As long as the data contract from Step 1 is met, the rest of the optimization and training pipeline will run smoothly with your new sample.

## Expected Output

After a successful run, a new directory will be created in your GitHub repository with a path similar to:
`PIRIS_PIPELINE/Results_from_YYYY-MM-DD_HH-MM-SS_run`

This directory will contain all the generated plots from the simulation runs in PDF format, such as:
-   `Parameter_importance_[sample_name].pdf`
-   `final_state_[sample_name].pdf`
-   `loss_evolution_[sample_name].pdf`
-   `scaling_analysis_piris_vs_dft.pdf`

## Dependencies

The primary Python libraries used in this project are:
-   `tensorflow`
-   `optuna`
-   `scikit-learn`
-   `pandas`
-   `numpy`
-   `matplotlib`
-   `seaborn`
-   `kaleido` (for saving Plotly figures)
