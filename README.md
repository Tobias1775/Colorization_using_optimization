### Project Description

This project implements the algorithm from the paper "Colorization using Optimization" by Anat Levin, Dani Lischinski, and Yair Weiss (2004). The goal of the algorithm is to add color to grayscale images using a small number of color scribbles provided by the user. The key idea is to propagate these colors to the entire image in a way that respects the structure and edges present in the grayscale image.

### Detailed Comments

1. **Introduction to the Algorithm:**
   - The algorithm takes a grayscale image and a few color scribbles as input.
   - The colorization process involves propagating the user-provided colors throughout the image.
   - The propagation respects image edges to maintain object boundaries and details.

2. **Optimization Framework:**
   - The core of the algorithm is based on an optimization framework.
   - It minimizes a cost function that ensures smooth color transitions while preserving edges.
   - The cost function incorporates a weighting term that penalizes color differences across strong edges.

3. **Mathematical Formulation:**
   - The optimization problem is formulated as a quadratic minimization problem.
   - Let \(I\) be the grayscale image, and \(C\) be the color image to be estimated.
   - The cost function \(E(C)\) is defined as:
     \[
     E(C) = \sum_{i,j} W_{ij} (C_i - C_j)^2
     \]
     where \(W_{ij}\) are weights derived from the grayscale image \(I\), and \(C_i\) and \(C_j\) are colors at pixels \(i\) and \(j\), respectively.

4. **Weight Calculation:**
   - The weights \(W_{ij}\) are computed based on the intensity differences in the grayscale image.
   - High weights are assigned to pixel pairs with similar intensities, and low weights to those with different intensities.
   - This ensures that colors are propagated smoothly within regions of similar intensity but are restricted across edges.

5. **User Interaction:**
   - The user provides initial color scribbles on the grayscale image.
   - These scribbles act as constraints in the optimization problem.
   - The algorithm uses these constraints to guide the color propagation process.

6. **Implementation Details:**
   - The project is implemented in Python using libraries such as NumPy and OpenCV.
   - The optimization problem is solved using efficient numerical solvers.
   - The user interface allows for easy input of color scribbles and visualization of the colorized image.

7. **Expected Outcome:**
   - The output is a colorized version of the grayscale image that looks natural and visually appealing.
   - The algorithm effectively preserves edges and details, resulting in a high-quality colorization.

This detailed description and comments provide a rough understanding of the colorization algorithm using optimization. The project aims to faithfully implement the techniques proposed in the 2004 paper, offering a practical tool for image colorization.
