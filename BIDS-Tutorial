# The BIDS Tool Ecosystem -- A Plain-Language Guide

**What every neuroimaging analysis tool does, why it does it, and how to run it without Docker**

Version 0.1 -- May 2026
Epistemic Systems Lab (ESL) / W3C AIKR CG
---

## Why This Document Exists

The Brain Imaging Data Structure (BIDS) is a standard way to organize brain imaging data so that software tools can automatically find and process it. Over the past decade, an ecosystem of ~40+ tools has grown around this standard. The problem is that the ecosystem's own documentation is nearly impenetrable -- the official BIDS Apps page shows Docker build status badges rather than explaining what each tool actually does.

This document provides three things:

1. A plain-language explanation of every major BIDS tool -- what scientific question it answers, what math it uses, and what goes in and comes out
2. An assessment of whether each function can run in a browser (Colab/Vercel) without Docker
3. An architectural blueprint for "BIDS Academy" -- a browser-based learning environment where each analysis function comes with a tutorial covering the science, the math, and the code
---

## How Brain Imaging Analysis Works -- The Big Picture

Brain imaging produces raw signals (radio waves from MRI scanners, electrical potentials from EEG electrodes, photon counts from PET tracers). These signals must go through a long chain of processing before a scientist can say anything about how the brain works.

The chain looks like this:

```
RAW SCANNER OUTPUT
    |
    v
[CONVERSION] -- Transform proprietary scanner formats into standardized files
    |
    v
[VALIDATION] -- Check that the files follow the BIDS standard
    |
    v
[QUALITY CONTROL] -- Detect artifacts, motion, signal problems
    |
    v
[PREPROCESSING] -- Remove noise, align to standard brain space, correct distortions
    |
    v
[FEATURE EXTRACTION] -- Measure cortical thickness, connectivity, activation patterns
    |
    v
[STATISTICAL ANALYSIS] -- Test hypotheses, classify conditions, build models
    |
    v
SCIENTIFIC CONCLUSIONS
```

Each BIDS App handles one or more of these stages. Docker containers bundle each app with its dependencies so you can run them without installing dozens of packages -- but every app is built on open-source libraries that can be used independently.


---

## LAYER 1 -- DATA CONVERTERS

These tools transform raw scanner output into BIDS-compliant directory structures.


### 1.1 dcm2niix

**What it does**: Converts DICOM files (the native format of MRI scanners) into NIfTI files (the standard neuroimaging format) plus JSON sidecar metadata.

**The science**: MRI scanners produce data as 2D slices acquired over time. dcm2niix reassembles these into 3D (or 4D, for time series) volumes, handling vendor-specific encoding differences (Siemens, GE, Philips all store DICOMs differently).

**The math**: Primarily coordinate transformations -- converting from scanner coordinates to a standardized patient coordinate system using affine transformation matrices (4x4 matrices encoding rotation, translation, and scaling).

**Input**: DICOM directory (.dcm files)
**Output**: NIfTI files (.nii.gz) + JSON metadata (.json)

**Browser-runnable?**: Partially. The core conversion is C code; a WASM port could work but doesn't exist yet. However, if you already have NIfTI files (as most shared datasets do), you skip this entirely.

**Python alternative**: `pip install dcm2niix` (wrapper) or use nibabel for direct NIfTI manipulation.


### 1.2 HeuDiConv (Heuristic DICOM Converter)

**What it does**: Wraps dcm2niix with a heuristic system that automatically maps scanner sequences to BIDS naming conventions (e.g., "MPRAGE" becomes "sub-01/anat/sub-01_T1w.nii.gz").

**The science**: Different labs name their scanner sequences differently. HeuDiConv lets you write rules (heuristics) that map your lab's naming to BIDS conventions.

**The math**: Pattern matching and file system operations -- no signal processing.

**Input**: DICOM directory + heuristic file (Python)
**Output**: BIDS-organized dataset

**Browser-runnable?**: Yes, the heuristic logic is pure Python. The DICOM reading can use pydicom.

**Python alternative**: `pip install heudiconv`


### 1.3 BIDScoin

**What it does**: GUI-based converter that auto-discovers your data structure and lets you visually map it to BIDS without writing code.

**The science**: Same as HeuDiConv but with automatic header inspection to guess mappings.

**Input**: Source data in any supported format
**Output**: BIDS dataset

**Browser-runnable?**: The GUI could be reimplemented as a web app. The backend logic is Python.

**Python alternative**: `pip install bidscoin`

---
### 1.4 MNE-BIDS

**What it does**: Converts electrophysiology data (EEG, MEG, iEEG) to BIDS format.

**The science**: EEG/MEG data has different structure from MRI -- channels rather than voxels, continuous time series rather than volumes. MNE-BIDS handles electrode positions, event markers, and channel metadata.

**Input**: EEG/MEG recordings in various formats (EDF, BrainVision, FIF, etc.)
**Output**: BIDS-organized electrophysiology dataset

**Browser-runnable?**: Yes -- MNE-Python is pure Python/NumPy.

**Python alternative**: `pip install mne-bids`


### 1.5 phys2bids / bidsphysio

**What it does**: Converts physiological recordings (heart rate, respiration, skin conductance) to BIDS format.

**The science**: Physiological signals recorded alongside brain imaging are used to regress out body-related noise from brain signals. These tools standardize the format.

**Input**: Physiological recording files
**Output**: BIDS-compliant .tsv.gz physiological data

**Browser-runnable?**: Yes -- pure Python.


---

## LAYER 2 -- VALIDATION

### 2.1 BIDS Validator

**What it does**: Checks whether a dataset actually conforms to the BIDS specification -- correct file names, required metadata present, consistent dimensions.

**The science**: Specification compliance checking. No analysis -- pure structural validation.

**The math**: None -- this is file system inspection and JSON schema validation.

**Input**: A directory that claims to be a BIDS dataset
**Output**: List of errors and warnings

**Browser-runnable?**: YES -- already runs in the browser at bids-standard.github.io/bids-validator. Written in JavaScript.

**Python alternative**: `pip install bids-validator` (CLI version)


---

## LAYER 3 -- QUALITY CONTROL

### 3.1 MRIQC (MRI Quality Control)

**What it does**: Generates quantitative quality metrics and visual reports for structural and functional MRI data. Answers: "Is this scan usable, or is it too noisy/motion-corrupted?"

**The science**: Quality assessment is based on established image quality metrics (IQMs) that quantify signal-to-noise ratio, contrast, spatial artifacts, and subject motion. These metrics help researchers decide whether to include or exclude a scan before spending hours processing it.

**Key metrics and their math**:

- **Signal-to-Noise Ratio (SNR)**: Mean signal intensity divided by the standard deviation of background noise. SNR = mu_signal / sigma_noise. Higher is better.

- **Contrast-to-Noise Ratio (CNR)**: Difference in mean intensity between tissue types (gray matter vs white matter) divided by noise. CNR = |mu_GM - mu_WM| / sigma_noise. Measures how well you can distinguish tissue boundaries.

- **Entropy Focus Criterion (EFC)**: Shannon entropy of the image voxel intensities. High entropy suggests ghosting or ringing artifacts. EFC = -sum(p_i * log(p_i)) where p_i is the normalized intensity histogram.

- **Framewise Displacement (FD)** (for functional MRI): How much the head moved between consecutive volumes, computed as the sum of absolute derivatives of the 6 rigid-body motion parameters (3 translations + 3 rotations). FD_t = |delta_x| + |delta_y| + |delta_z| + |delta_alpha| + |delta_beta| + |delta_gamma|. Spikes indicate sudden head jerks.

- **DVARS**: The root-mean-square change in BOLD signal intensity between consecutive volumes across the whole brain. DVARS_t = sqrt(mean((S_t - S_{t-1})^2)). High values suggest motion or scanner artifacts.

- **Carpet plots**: 2D visualizations where rows are voxels (grouped by tissue type) and columns are time points, colored by signal intensity. Global signal drifts and motion-related artifacts appear as vertical stripes.

**Input**: BIDS dataset (T1w and/or BOLD images)
**Output**: JSON quality metrics per image + HTML visual reports

**Browser-runnable?**: YES for the metrics. SNR, CNR, EFC, FD, and DVARS are all NumPy/SciPy operations. The full MRIQC pipeline includes skull stripping and tissue segmentation (heavier), but the core QC metrics can absolutely run in Colab.

**Python alternative**: nilearn + nibabel + custom metric functions. `pip install mriqc` also works without Docker.


---

## LAYER 4 -- PREPROCESSING

This is where the heavy lifting happens. Preprocessing removes artifacts and transforms brain images into a common coordinate space so you can compare across subjects.


### 4.1 fMRIPrep (fMRI Preprocessing)

**What it does**: The dominant preprocessing pipeline for functional MRI. Takes raw BOLD time series and anatomical scans, produces cleaned, spatially normalized data ready for statistical analysis.

**The science**: Raw fMRI data is contaminated by head motion, magnetic field inhomogeneities, physiological noise (heartbeat, breathing), and scanner drift. fMRIPrep applies a sequence of corrections, drawing from the best algorithms across multiple software packages.

**The preprocessing steps and their math**:

1. **Skull stripping** -- Removes non-brain tissue (skull, eyes, neck) from anatomical images.
   - Method: ANTs brain extraction or FreeSurfer watershed algorithm
   - Math: Morphological operations (erosion/dilation) + atlas-based template matching using diffeomorphic registration

2. **Tissue segmentation** -- Classifies each voxel as gray matter (GM), white matter (WM), or cerebrospinal fluid (CSF).
   - Method: FSL FAST (FMRIB Automated Segmentation Tool)
   - Math: Hidden Markov Random Field model with Expectation-Maximization. Each voxel's intensity is modeled as a mixture of Gaussians (one per tissue class), with spatial regularization from neighboring voxels: P(class_i | intensity_i, neighbors) proportional to P(intensity_i | class_i) * P(class_i | neighbors)

3. **Surface reconstruction** -- Builds a 3D mesh of the cortical surface (the wrinkled sheet of gray matter).
   - Method: FreeSurfer recon-all
   - Math: Deformable surface models -- an initial spherical mesh is iteratively deformed to fit intensity gradients in the MRI. The surface energy function balances data fit (intensity gradient) against smoothness (curvature penalty): E = E_data + lambda * E_smoothness

4. **Motion correction** -- Aligns all functional volumes to a reference volume, correcting for head movement during the scan.
   - Method: FSL MCFLIRT or ANTs
   - Math: Rigid-body registration -- finds the 6 parameters (3 translations, 3 rotations) that minimize the cost function (mutual information or correlation ratio) between each volume and the reference: min_{R,t} C(V_t, R*V_ref + t)

5. **Susceptibility distortion correction** -- Corrects spatial warping caused by magnetic field inhomogeneities near air-tissue interfaces (sinuses, ear canals).
   - Method: FSL TOPUP (using reversed phase-encode fieldmaps) or SyN-SDC (fieldmap-free)
   - Math: Estimates a voxel displacement field by comparing images acquired with opposite phase-encode directions. The displacement field is modeled as a spline and optimized to make the two images match after unwarping.

6. **Coregistration** -- Aligns the functional images to the anatomical image (they have different resolutions and contrasts).
   - Method: FreeSurfer bbregister or FSL FLIRT
   - Math: Boundary-based registration -- optimizes alignment by maximizing the intensity contrast across the white matter boundary in the functional image: Cost = sum over boundary vertices of (I_func(v + epsilon*n) - I_func(v - epsilon*n))^2

7. **Spatial normalization** -- Warps each subject's brain into a standard template space (e.g., MNI152) so you can compare voxels across people.
   - Method: ANTs SyN (Symmetric Normalization)
   - Math: Diffeomorphic registration -- finds a smooth, invertible deformation field phi that maps the subject's anatomy to the template. The deformation is parameterized as the integral of a velocity field: phi = integral_0^1 v(phi_t, t) dt. The optimization minimizes: E = Similarity(I_moving(phi), I_template) + Regularization(phi)

8. **Confound estimation** -- Computes nuisance regressors (motion parameters, physiological signals, global signals) that can be regressed out during statistical analysis.
   - Method: CompCor (Component-based noise correction)
   - Math: PCA on the BOLD time series from WM and CSF voxels (which shouldn't contain neural signal). The top principal components capture physiological noise patterns.

**Input**: BIDS dataset with T1w anatomical + BOLD functional images (+ optional fieldmaps)
**Output**: Preprocessed BOLD in template space, confound regressors, QC reports

**Browser-runnable?**: PARTIALLY. The individual mathematical operations (rigid-body registration, PCA, spatial transformations) are all NumPy/SciPy. But the full pipeline requires FreeSurfer (6+ hours per subject) and ANTs (large memory). A tutorial version showing each step on downsampled data -- absolutely yes. Full production runs -- need Colab Pro or HPC.

**Python alternative**: nipype workflows using nilearn, nibabel, ANTs (via antspy), FreeSurfer (local install). `pip install fmriprep` works but needs FreeSurfer license.


### 4.2 HCP Pipelines (Human Connectome Project)

**What it does**: The preprocessing pipeline developed for the Human Connectome Project -- the gold standard for high-resolution multimodal brain imaging.

**The science**: Designed for HCP-style acquisitions (0.7mm resolution T1w/T2w, multiband fMRI, high angular resolution diffusion). More demanding than fMRIPrep but handles multimodal data (structural + functional + diffusion) in a unified framework.

**Key differences from fMRIPrep**:
- Requires both T1w AND T2w anatomical scans
- Uses the T2w for improved myelin mapping (T1w/T2w ratio correlates with myelin content)
- Produces CIFTI format outputs (surface-based for cortex, volumetric for subcortex)
- Includes diffusion preprocessing

**Input**: BIDS dataset with T1w + T2w + BOLD + optional DWI
**Output**: Preprocessed data in CIFTI grayordinates space

**Browser-runnable?**: No for full pipeline. The myelin mapping and CIFTI concepts could be taught in Colab.


### 4.3 BrainSuite

**What it does**: Integrated pipeline for structural, diffusion, and functional MRI processing with built-in quality control at each stage.

**The science**: BrainSuite's distinctive feature is its iterative approach -- you can inspect and manually correct results at each step (e.g., fix skull-stripping errors before proceeding to segmentation).

**Math highlights**:
- **BFC (Bias Field Correction)**: Models the intensity inhomogeneity (caused by RF coil sensitivity variations) as a smooth multiplicative field, estimated via B-spline fitting
- **BSE (Brain Surface Extractor)**: Edge detection + morphological operations + connected component analysis
- **SVReg (Surface-Volume Registration)**: Simultaneous registration of cortical surfaces and subcortical volumes to an atlas

**Browser-runnable?**: Partial -- the QC visualization and bias field estimation could work in Colab.


---

## LAYER 5 -- STRUCTURAL ANALYSIS

### 5.1 FreeSurfer (BIDS App)

**What it does**: Cortical surface reconstruction and parcellation -- builds detailed 3D models of the cortical surface and divides it into anatomical regions.

**The science**: The cortex is a ~2-4mm thick sheet of gray matter, highly folded. FreeSurfer models this as two surfaces: the pial surface (outer boundary, touching CSF) and the white surface (inner boundary, touching white matter). Between these surfaces, it measures cortical thickness, surface area, curvature, and local gyrification.

**Key computations**:

- **Cortical thickness**: The shortest distance between the white and pial surfaces at each vertex. Measured in millimeters. Thinning of specific regions correlates with Alzheimer's disease, aging, and various neurological conditions.

- **Parcellation**: Assigns each surface vertex to one of ~70 anatomical regions (e.g., superior temporal gyrus, precentral gyrus) using a probabilistic atlas. Method: Bayesian classification using both geometric features (sulcal depth, curvature) and intensity profiles.

- **Subcortical segmentation**: Classifies deep brain structures (hippocampus, amygdala, thalamus, caudate, putamen) using a probabilistic atlas with shape priors.

- **Longitudinal pipeline**: For repeated scans of the same person over time. Creates a within-subject template and measures change. Math: Inverse-consistent registration where forward and backward transformations are computed simultaneously.

**Input**: BIDS dataset with T1w (optionally T2w, FLAIR)
**Output**: Surface meshes, parcellation labels, volume/thickness/area statistics per region

**Browser-runnable?**: NO for full recon-all (6-12 hours per subject). YES for visualizing and analyzing FreeSurfer outputs (the parcellation statistics are just CSV tables, surfaces can be rendered with nilearn).


### 5.2 MAGeTbrain (Multiple Automatically Generated Templates)

**What it does**: High-resolution segmentation of subcortical structures (hippocampus subfields, thalamic nuclei, cerebellar lobules).

**The science**: Standard atlases have limited resolution for small structures. MAGeTbrain uses a multi-atlas approach: it propagates labels from a small set of manually segmented "gold standard" brains through a set of template brains to the target, then fuses the labels by majority voting.

**The math**: Multi-atlas label fusion. For each voxel, multiple atlas segmentations are warped to the target space and combined: Label(x) = argmax_L sum_i w_i * delta(atlas_i(x) = L), where w_i are weights based on local image similarity.

**Input**: BIDS dataset with T1w
**Output**: Segmentation labels for subcortical structures

**Browser-runnable?**: The label fusion step (majority voting) is trivial. The registration is heavy.


---

## LAYER 6 -- CONNECTIVITY AND NETWORK ANALYSIS

### 6.1 giga_connectome

**What it does**: Generates functional connectomes (correlation matrices) from fMRIPrep outputs.

**The science**: The brain is organized as a network. Functional connectivity measures how strongly different regions' activity fluctuates together over time. If two regions consistently activate and deactivate in sync, they're considered "functionally connected."

**The math**:
1. Extract mean BOLD time series from each brain region (using a parcellation atlas like Schaefer, AAL, or DiFuMo)
2. Compute pairwise Pearson correlation between all region pairs: r_ij = cov(ts_i, ts_j) / (sigma_i * sigma_j)
3. Optionally apply Fisher z-transform: z_ij = 0.5 * ln((1+r_ij)/(1-r_ij)) to make correlations normally distributed
4. Result: a symmetric N x N matrix (where N = number of brain regions)

This is the representation that COEVO works with -- the Cetron et al. dataset contains exactly these kinds of representational dissimilarity matrices (300 parcels, 66-value condensed distance vectors per subject).

**Input**: fMRIPrep derivatives (preprocessed BOLD + confound regressors)
**Output**: Connectivity matrices (N x N per subject)

**Browser-runnable?**: YES -- this is pure NumPy/nilearn. Already runs in Colab perfectly.

**Python alternative**: `nilearn.connectome.ConnectivityMeasure` -- literally a few lines of code.


### 6.2 MRtrix3_connectome

**What it does**: Generates structural connectomes from diffusion MRI data -- mapping the physical white matter tracts connecting brain regions.

**The science**: Diffusion MRI measures how water molecules diffuse in brain tissue. In white matter tracts, water diffuses preferentially along the fiber direction (like water flowing along a bundle of straws). By tracing these directions, you can reconstruct the brain's wiring diagram.

**Key computations**:

- **Fiber Orientation Distribution (FOD) estimation**: At each voxel, estimate the distribution of fiber orientations using constrained spherical deconvolution (CSD). Math: The diffusion signal S(g) is modeled as the convolution of the FOD f(theta, phi) with a single-fiber response function R: S(g) = integral f(theta, phi) * R(g, theta, phi) d(theta, phi). The FOD is recovered by deconvolution, expressed in spherical harmonics.

- **Tractography**: Starting from seed points, follow the FOD to trace streamlines through the brain. At each step: x_{t+1} = x_t + delta * direction(FOD(x_t)). With probabilistic tractography, the direction is sampled from the FOD rather than taking the peak, generating many possible paths.

- **Connectome construction**: Count the number of streamlines connecting each pair of brain regions. The structural connectome matrix S_ij = number of streamlines between regions i and j.

**Input**: BIDS dataset with DWI (diffusion-weighted images)
**Output**: Structural connectome matrices, tractography files

**Browser-runnable?**: PARTIAL. The matrix construction from precomputed tractography is trivial (NumPy). The tractography itself is computationally expensive but the mathematics (stepping along vector fields) could be demonstrated on 2D slices in Colab.


### 6.3 Connectome Mapper 3 (CMP3)

**What it does**: Full pipeline from raw data to multi-resolution connectomes -- covers anatomical, diffusion, functional, and EEG processing.

**The science**: Provides connectomes at multiple spatial resolutions (e.g., 83, 129, 234, 463, 1015 regions) using the Lausanne parcellation scheme. This matters because network properties can change depending on the granularity of your parcellation.

**Input**: BIDS dataset with T1w + DWI and/or BOLD and/or EEG
**Output**: Connectome matrices at multiple resolutions

**Browser-runnable?**: The multi-resolution concept and matrix analysis -- yes. Full pipeline -- no.


### 6.4 ndmg (NeuroData's MRI to Graphs)

**What it does**: End-to-end pipeline from structural MRI and diffusion to brain graphs (connectomes represented as graph data structures).

**The science**: Represents the brain as a mathematical graph where nodes are brain regions and edges are structural connections. Enables graph-theoretic analysis (small-worldness, modularity, hub detection).

**Graph metrics**:
- **Degree**: Number of connections per node. d_i = sum_j A_ij
- **Clustering coefficient**: How much a node's neighbors connect to each other. C_i = 2 * E_i / (k_i * (k_i - 1)) where E_i is the number of edges among node i's neighbors
- **Path length**: Shortest path between any two nodes
- **Modularity**: How well the network divides into communities. Q = (1/2m) * sum_{ij} [A_ij - k_i*k_j/(2m)] * delta(c_i, c_j)

**Input**: BIDS dataset with T1w + DWI
**Output**: Graph files, graph metrics

**Browser-runnable?**: YES for graph analysis (networkx, scipy.sparse). The MRI processing stages need local tools.


---

## LAYER 7 -- SPECIALIZED ANALYSIS TOOLS

### 7.1 SPM (Statistical Parametric Mapping) BIDS App

**What it does**: Classic neuroimaging analysis software (originally MATLAB). Statistical analysis of brain images -- identifies which brain regions activate during specific tasks or differ between groups.

**The science**: The General Linear Model (GLM) applied to every voxel independently. For each voxel: Y = X*beta + epsilon, where Y is the time series, X is the design matrix (encoding experimental conditions), beta are the parameters to estimate, and epsilon is noise. A t-statistic is computed for each voxel to test whether a condition's effect is significantly different from zero.

**The math**: Mass-univariate GLM + Random Field Theory for multiple comparisons correction. Because you're testing ~100,000 voxels simultaneously, you need to correct for multiple comparisons. RFT models the statistical map as a smooth random field and computes the probability of getting clusters of a given size by chance: P(cluster > k) = E[number of clusters above threshold] * P(cluster size > k | cluster exists).

**Input**: BIDS dataset (preprocessed)
**Output**: Statistical parametric maps (t-maps, F-maps), thresholded activation maps

**Browser-runnable?**: YES using nilearn's GLM module. `nilearn.glm.first_level` and `nilearn.glm.second_level` provide the same GLM framework in Python without MATLAB.


### 7.2 Hyperalignment

**What it does**: Aligns brain activation patterns across subjects in a high-dimensional feature space, enabling better cross-subject comparison.

**The science**: Different people's brains are anatomically different -- even after spatial normalization, the same cognitive function may map to slightly different voxel patterns. Hyperalignment finds a rotation in voxel space that aligns subjects' representational geometries.

**The math**: Procrustes analysis extended to multiple subjects. For each subject, find rotation matrix R_i that minimizes: sum_i ||X_i * R_i - X_template||^2, where X_i is subject i's voxel-by-condition response matrix. Solved iteratively: estimate template, align each subject to template, update template, repeat.

This is directly relevant to COEVO -- the representational dissimilarity matrices from Cetron et al. are the starting point for exactly this kind of cross-subject alignment analysis.

**Input**: BIDS derivatives (preprocessed BOLD, typically from a shared stimulus paradigm)
**Output**: Rotation matrices per subject, aligned activation patterns

**Browser-runnable?**: YES -- this is linear algebra (SVD/Procrustes). PyMVPA or custom NumPy implementation works in Colab.


### 7.3 deepMReye

**What it does**: Decodes eye position from fMRI data without an eye tracker, using deep learning.

**The science**: Eye movements during scanning confound fMRI results and are normally tracked with expensive MR-compatible eye trackers. deepMReye uses a convolutional neural network trained on simultaneous fMRI + eye tracking data to predict gaze position from brain images alone.

**The math**: 3D CNN (convolutional neural network) applied to the eyeball region of fMRI volumes. Architecture: 3D convolutions + batch norm + ReLU + fully connected layers. Loss: mean squared error between predicted and actual gaze coordinates.

**Input**: BIDS dataset (BOLD images)
**Output**: Predicted eye position time series

**Browser-runnable?**: YES with TensorFlow.js or a pre-trained model in Colab. Inference is lightweight.


### 7.4 PRFmodel (Population Receptive Field)

**What it does**: Estimates the visual receptive field properties of each voxel in visual cortex -- what part of the visual field each voxel "sees."

**The science**: Neurons in visual cortex respond to specific parts of the visual field. A population receptive field (pRF) is the aggregate receptive field of all neurons contributing to one fMRI voxel. Estimated by presenting visual stimuli at many positions and fitting a model to the response.

**The math**: For each voxel, fit a 2D Gaussian receptive field model: pRF(x, y) = A * exp(-((x-x0)^2 + (y-y0)^2) / (2*sigma^2)), where x0, y0 are the receptive field center and sigma is the size. The predicted time series is the convolution of this Gaussian with the stimulus apertures, convolved with the hemodynamic response function.

**Input**: BIDS dataset with retinotopic mapping stimuli
**Output**: Maps of pRF center (eccentricity, polar angle) and size

**Browser-runnable?**: YES -- the Gaussian fitting is scipy.optimize. Could make a beautiful interactive visualization.


---

## LAYER 8 -- SUPPORTING TOOLS (Pure Python, No Containers)

### 8.1 PyBIDS

**What it does**: Parse and query BIDS datasets. Find files by subject, session, modality, task, etc.

**The math**: None -- file system traversal and metadata querying.

**Browser-runnable?**: YES. `pip install pybids`

### 8.2 nilearn

**What it does**: Machine learning for neuroimaging. Provides plotting, parcellation, GLM, connectivity, decoding.

**Key functions**: Signal extraction from brain regions, connectome computation, statistical maps, searchlight analysis, brain decoding.

**Browser-runnable?**: YES. `pip install nilearn` -- works perfectly in Colab.

### 8.3 nibabel

**What it does**: Read/write neuroimaging file formats (NIfTI, GIFTI, CIFTI, MGH).

**Browser-runnable?**: YES. `pip install nibabel`

### 8.4 nipype

**What it does**: Pipeline framework that wraps external tools (FSL, ANTs, FreeSurfer, SPM) into Python-scriptable workflows with dependency tracking and parallel execution.

**Browser-runnable?**: The framework itself is Python. Individual wrapped tools need local installation.

### 8.5 neurobagel

**What it does**: Cross-dataset query tool -- search across multiple BIDS datasets by clinical-demographic and imaging parameters.

**Browser-runnable?**: YES -- web interface already exists.

### 8.6 psychopy-bids

**What it does**: Automatically outputs experiment data (stimulus timing, responses) in BIDS format from PsychoPy experiments.

**Browser-runnable?**: PsychoPy has a web mode (Pavlovia).


---

## BROWSER-RUNNABILITY SUMMARY

### Fully runnable in Colab (no installation beyond pip):

| Function | Library | Lines of code |
|---|---|---|
| BIDS validation | bids-validator | ~5 |
| Dataset querying | PyBIDS | ~10 |
| Read/write brain images | nibabel | ~5 |
| Quality metrics (SNR, CNR, FD, DVARS) | NumPy/nibabel | ~50 |
| Tissue segmentation (basic) | nilearn | ~20 |
| Functional connectivity matrices | nilearn | ~15 |
| GLM / statistical maps | nilearn.glm | ~30 |
| Graph analysis of connectomes | networkx | ~20 |
| Hyperalignment (Procrustes) | NumPy (SVD) | ~40 |
| pRF fitting | SciPy optimize | ~60 |
| Brain visualization | nilearn.plotting | ~5 |
| Representational similarity analysis | NumPy/SciPy | ~30 |
| Machine learning decoding | nilearn.decoding | ~25 |


### Partially runnable (need downsampled data or simplified versions):

| Function | What works | What doesn't |
|---|---|---|
| Skull stripping | antspyx (slow but works) | FreeSurfer watershed |
| Motion correction | nilearn (basic) | ANTs SyN (memory) |
| Spatial normalization | antspyx (Colab Pro) | Full resolution |
| Diffusion FOD estimation | dipy | Full tractography at scale |
| Surface reconstruction | Partial via FreeSurfer dev | Full recon-all |


### Requires local/HPC (not browser-feasible):

| Function | Why |
|---|---|
| FreeSurfer recon-all | 6-12 hours, high memory |
| Full fMRIPrep pipeline | Orchestrates many heavy tools |
| Full tractography (millions of streamlines) | Computationally intensive |
| DICOM conversion from raw scanner data | Usually done at the scanner |


---

## BIDS ACADEMY -- ARCHITECTURAL BLUEPRINT

### The Vision

A browser-based learning environment where each neuroimaging analysis function comes with:

1. **Concept explainer** -- What scientific question does this answer? (2 minutes reading)
2. **Math tutorial** -- What computation is being performed? Interactive equations with visual explanations
3. **Code tutorial** -- Run the actual analysis in Colab on sample data
4. **Connection map** -- How does this function relate to others in the pipeline?

### Technical Architecture

**Front end (Vercel/GitHub Pages)**:
- Interactive ecosystem map (React/D3 -- clickable pipeline diagram)
- Explainer pages per tool (Markdown rendered as clean HTML)
- "Launch in Colab" buttons for each function

**Back end (Google Colab notebooks)**:
- One notebook per function (e.g., "01_quality_metrics.ipynb", "02_motion_correction.ipynb")
- Each notebook uses a small sample BIDS dataset (ds000003 from OpenNeuro -- 13 subjects, simple task)
- Each notebook structure:
  - Section 1: The Science (why we do this)
  - Section 2: The Math (interactive equations with plots)
  - Section 3: The Code (run it yourself)
  - Section 4: Exercises (try modifying parameters)
  - Section 5: Connection to the pipeline (what comes next)

**Sample dataset**: ds000003 or ds000114 from OpenNeuro (small, public, well-validated)

### Notebook Sequence

```
00_what_is_bids.ipynb           -- BIDS structure, PyBIDS, validation
01_reading_brain_images.ipynb   -- nibabel, NIfTI format, coordinate systems
02_quality_control.ipynb        -- SNR, CNR, FD, DVARS, carpet plots
03_skull_stripping.ipynb        -- Brain extraction, morphological operations
04_tissue_segmentation.ipynb    -- Gaussian mixtures, EM algorithm
05_motion_correction.ipynb      -- Rigid-body registration, cost functions
06_spatial_normalization.ipynb  -- Template spaces, deformation fields
07_functional_connectivity.ipynb -- Correlation matrices, parcellations
08_glm_activation.ipynb         -- General Linear Model, statistical maps
09_structural_connectomes.ipynb -- Diffusion, tractography basics
10_graph_analysis.ipynb         -- Network metrics, modularity
11_hyperalignment.ipynb         -- Cross-subject alignment, Procrustes
12_machine_learning.ipynb       -- Decoding, SVM, cross-validation
13_representational_similarity.ipynb -- RSA, RDMs, connection to COEVO

### AIKR CG Contribution

This project is a case study for AIKR CG Technical Note TN3: "Making Tool Ecosystems Machine-Readable and Human-Accessible." The BIDS Apps page fails because it describes tools by their operational status (Docker build passing/failing) rather than by their function, input/output, and scientific basis. An AIKR-style approach would:

1. Define a tool description schema (extending schema.org/SoftwareApplication)
2. Include fields for: scientific_function, mathematical_basis, input_format, output_format, browser_runnability, tutorial_url
3. Generate both human-readable documentation and machine-consumable metadata from the same source
4. Demonstrate this on the BIDS ecosystem as proof of concept


---



## Next Steps

1. Build the interactive ecosystem
2. Create Notebook 00 (What is BIDS) and Notebook 07 (Functional Connectivity) as proof of concept
3. Draft AIKR CG Technical Note TN3 proposal



---

*Document produced by ESL / Anthropomorphic Press, May 2026*
*License: CC BY 4.0*
