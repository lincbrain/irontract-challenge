# Irontract Challenge

This repository allows you to evaluate the accuracy of your diffusion MRI (dMRI) tractography pipeline against anatomic tracing in the same brains, using the dMRI and tracing data that were used in the [IronTract Challenge](https://irontract.mgh.harvard.edu/). Follow the steps below to upload your tractography results and see your receiver operating characteristic (ROC) curve plotted against those of the other teams.

## Instructions

1. [Download the dMRI datasets](https://dandiarchive.org/dandiset/001289?search=irontract&pos=1) from the DANDI archive. Subjects MR256 and MR243 are, respectively, the training and validation case that were used in the IronTract Challenge (see paper below for details). Each dataset includes dMRI data for the two acquisition schemes that were used in the Challenge, Cartesian (`derivatives/*/dwi/*acq-DSI*`) and multi-shell (`derivatives/*/dwi/*acq-MulShell*`), as well as the injection site as a binary mask (`derivatives/*/micr/*injection.nii.gz`).
2. Run your tractography pipeline on the dMRI data, identify the streamlines that go through the injection site mask, and save those streamlines as a binary NIfTI volume that indicates which voxels were visited by the streamlines. You will need to vary some parameter in your tractography method (in the challenge most teams varied the bending angle threshold, but you can vary a different parameter if you prefer), rerun your tractography pipeline with each value to produce multiple NIfTI volumes. This is important to provide different operating points along the ROC curve - if you only upload a single volume, you will get a single false positive and true positive value, which will not be enough for computing an area under the curve (AUC) and comparing your result against those of the other teams. Please make sure that the resolution, matrix size, and orientation information in the header of the tractography volumes that you upload matches that of the dMRI volumes that you downloaded.
3. When you are ready to upload your volumes, make a fork of this repo.
4. Save your volumes under the `submissions` directory.
5. Make a pull request (PR) into this repo, which will trigger the workflow.
6. A Github Action will be run to compare your tractography against the ground truth tracing. Your result will appear in a comment in your PR, and will also be saved in this repo.
7. If you report your result in a publication, please cite the paper below.

## Leaderboard

<!-- START_LEADERBOARD -->

| Rank | Username | AUC Score |
|------|----------|-----------|
| 1 | kabilar | 0.2222 |

<!-- END_LEADERBOARD -->


## Reference:
C. Maffei, G. Girard, K.G. Schilling, D.B. Aydogan, N. Adluru, A. Zhylka, Y. Wu, M. Mancini, A. Hamamci, A. Sarica, A. Teillac, S.H. Baete, D. Karimi, F.-C. Yeh, M.E. Yildiz, A. Gholipour,  Y. Bihan-Poudec, B. Hiba, A. Quattrone, A. Quattrone, P.-T. Yap, A. de Luca, J. Pluim, A. Leemans, V. Prabhakaran, B.B. Bendlin, A.L. Alexander, B.A. Landman, E.J. Canales-Rodríguez, M. Barakovic,  J. Rafael-Patino, T. Yu, G. Rensonnet, S. Schiavi, A. Daducci, M. Pizzolato, E. Fischi-Gomez, J.-P. Thiran, G. Dai, G. Grisot, N. Lazovski, S. Puch, M. Ramos, P. Rodrigues, V. Prchkovska, R. Jones, J. Lehman, S.N. Haber, A. Yendiki, [Insights from the IronTract challenge: optimal methods for mapping brain pathways from multi-shell diffusion MRI,](https://www.sciencedirect.com/science/article/pii/S1053811922004463) NeuroImage, 257:119327, 2022.
