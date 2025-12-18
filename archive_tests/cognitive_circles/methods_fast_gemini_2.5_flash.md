Alright, let's lay out the precise methodology for this project. Our goal is to understand how the temporal dynamics of hand-drawn circle kinematics reflect cognitive load and task performance. We'll achieve this by meticulously processing the raw data, extracting specific features, and performing targeted statistical analyses.

**I. Data Ingestion and Pre-processing**

1.  **Questionnaire Data Loading and Preparation:**
    *   Load the `data-from-trials.csv` file into a pandas DataFrame.
    *   Inspect column data types and ensure they are appropriate (e.g., `Participant ID` as categorical, Likert scales as numerical).
    *   Rename columns for clarity if necessary (e.g., `Task Perceived Mental Demand` to `Mental Demand`).
    *   Verify the range and distribution of Likert scale responses and objective performance metrics (`Correct Progress`, `Total Mistakes`).

2.  **Kinematic Trace Data Loading and Initial Cleaning:**
    *   For each of the 240 individual `.txt` files containing circle drawing traces:
        *   Parse the filename to extract `Participant ID`, `Task Type`, and `Task Difficulty`. This information is crucial for linking with the questionnaire data. Example: `P1-NumericalDifficult-02-08-2024-T11-47-20.498.txt` indicates Participant 1, Numerical Task, Difficult variant.
        *   Load the three columns (`timestamp`, `x-coordinate`, `y-coordinate`) into a DataFrame.
        *   Convert the `timestamp` column to a datetime object, then to seconds relative to the start of the recording for each task (i.e., the first timestamp of each file will be `t=0`).
        *   Inspect the raw `x` and `y` coordinates for obvious outliers (e.g., values far outside the expected tablet dimensions) or data acquisition errors. Based on initial EDA, we expect some noise inherent in tablet-based recordings.

3.  **Time Synchronization and Resampling:**
    *   Given the variable sampling rates common in such data, we will resample all kinematic traces to a consistent frequency, for example, 50 Hz. This will ensure uniform time steps for subsequent derivative calculations.
    *   Use linear interpolation for `x` and `y` coordinates to fill values at the new, fixed time points.

4.  **Noise Reduction (Smoothing):**
    *   To accurately calculate derivatives (velocity, acceleration, jerk) from potentially noisy sensor data, apply a Savitzky-Golay filter to the `x` and `y` coordinate time series independently.
    *   Based on prior work and initial data inspection, we will use a filter window size appropriate for the resampled data (e.g., 11-15 points) and a polynomial order of 3. This choice balances noise reduction with preservation of signal characteristics.

**II. Kinematic Feature Extraction**

1.  **Instantaneous Kinematic Features:**
    *   For each time point in the smoothed `x` and `y` time series:
        *   **Velocity:** Calculate the first derivative of `x` and `y` with respect to time (`vx = dx/dt`, `vy = dy/dt`). Then compute the magnitude of the instantaneous velocity: `Speed = sqrt(vx^2 + vy^2)`.
        *   **Acceleration:** Calculate the first derivative of `vx` and `vy` with respect to time (`ax = dvx/dt`, `ay = dvy/dt`). Then compute the magnitude of the instantaneous acceleration: `Acceleration = sqrt(ax^2 + ay^2)`.
        *   **Jerk:** Calculate the first derivative of `ax` and `ay` with respect to time (`jx = dax/dt`, `jy = day/dt`). Then compute the magnitude of the instantaneous jerk: `Jerk = sqrt(jx^2 + jy^2)`.
    *   All derivatives will be calculated using numerical differentiation methods suitable for evenly spaced time series.

2.  **Temporal Segmentation:**
    *   Divide the 2-minute (120-second) task duration into two distinct temporal phases:
        *   **Early Phase:** The first 60 seconds (0-60 seconds) of the circle-drawing task.
        *   **Late Phase:** The second 60 seconds (60-120 seconds) of the circle-drawing task.
    *   This segmentation allows us to analyze the "evolution" and "adaptation" of motor behavior over time as per the research question.

3.  **Segment-wise Feature Aggregation:**
    *   For each participant, for each task, and for each of the two temporal phases (Early, Late):
        *   Calculate the mean, standard deviation, and variance of the `Speed`, `Acceleration`, and `Jerk` magnitudes. These aggregated metrics will represent the kinematic profile for that specific phase of the task.
    *   Store these aggregated features in a structured format, indexed by `Participant ID`, `Task Type`, `Task Difficulty`, and `Phase` (Early/Late).

**III. Data Integration**

1.  **Merge Kinematic Features with Questionnaire and Performance Data:**
    *   Create a master DataFrame by merging the aggregated kinematic features (from Step II.C) with the questionnaire responses and objective performance metrics (from Step I.A).
    *   The merge will be performed using `Participant ID`, `Task Type`, and `Task Difficulty` as common keys.
    *   The resulting DataFrame will contain, for each participant and each of their 6 tasks, the `Task Perceived Mental Demand`, `Correct Progress`, `Total Mistakes`, `Task Type`, `Task Difficulty`, and the aggregated kinematic features for both the Early and Late phases.

**IV. Statistical Analysis**

1.  **Descriptive Statistics:**
    *   Compute descriptive statistics (mean, standard deviation, quartiles) for all extracted kinematic features, `Task Perceived Mental Demand`, `Correct Progress`, and `Total Mistakes`, segmented by `Task Type` and `Task Difficulty`. This will provide an overview of the data distributions.

2.  **Analysis of Temporal Changes in Kinematic Features:**
    *   For each kinematic feature (Speed, Acceleration, Jerk), calculate the difference between the Late and Early phases (`Delta_Speed = Mean_Speed_Late - Mean_Speed_Early`). This represents the change in motor behavior over the course of the task.

3.  **Correlation Analysis:**
    *   Perform Pearson correlation analyses to investigate the relationships between:
        *   **Kinematic features (Early and Late phases) and Subjective Workload:** Correlate `Mean_Speed_Early`, `Mean_Speed_Late`, `Mean_Acceleration_Early`, `Mean_Acceleration_Late`, `Mean_Jerk_Early`, `Mean_Jerk_Late` with `Task Perceived Mental Demand`.
        *   **Kinematic features (Early and Late phases) and Objective Performance:** Correlate the same kinematic features with `Correct Progress` and `Total Mistakes`.
        *   **Changes in Kinematic Features (Delta values) and Subjective Workload/Objective Performance:** Correlate `Delta_Speed`, `Delta_Acceleration`, `Delta_Jerk` with `Task Perceived Mental Demand`, `Correct Progress`, and `Total Mistakes`.
    *   These correlations will be performed for the entire dataset, and then separately for different `Task Type` and `Task Difficulty` categories to explore potential moderating effects.

4.  **Group Comparisons and Moderation Analysis:**
    *   Conduct a series of mixed-design ANOVAs or ANCOVAs to formally assess the impact of `Task Type` (Numerical, Sequential, Verbal) and `Task Difficulty` (Easy, Difficult) on the kinematic features and their temporal changes, while accounting for `Participant ID` as a random effect.
    *   Specifically, analyze:
        *   How `Task Type` and `Task Difficulty` affect `Mean_Speed`, `Mean_Acceleration`, and `Mean_Jerk` in both Early and Late phases.
        *   How `Task Type` and `Task Difficulty` influence the `Delta_Speed`, `Delta_Acceleration`, and `Delta_Jerk` values.
        *   Examine interaction effects between `Task Type`, `Task Difficulty`, and `Phase` (Early vs. Late) to understand if the temporal adaptation of motor behavior differs based on the cognitive task characteristics.
    *   Use `Task Perceived Mental Demand` as a covariate in some analyses to understand its influence on kinematic changes when controlling for task characteristics.

This systematic approach will allow us to rigorously test the hypothesis that temporal dynamics of hand-drawn circle kinematics reflect the evolution of cognitive load and task performance.