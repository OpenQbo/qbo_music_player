/*
 * COrbitObject.h
 *
 *  Created on: May 24, 2011
 *      Author: arturobc
 */

#ifndef CORBITOBJECT_H_
#define CORBITOBJECT_H_

#include <stdlib.h>
#include <iostream>
#include <vector>
#include <set>
#include <cmath>
#include <string>

#include <cv.h>
#include <highgui.h>
#include <cvaux.h>
#include <cxmisc.h>
#include <stdio.h>
#include <cxcore.h>
#include <cxtypes.h>
#include <climits>
#include <ml.h>

using namespace std;

class OrbitObject {
public:
	OrbitObject(string name="");
	virtual ~OrbitObject();

	vector<cv::Mat> images_;

	string name_;

	string images_dir_path_;

	cv::Mat descriptors_;

	cv::Ptr<CvSVM> svm_; //Used for Bag of Words Approach




};

#endif /* CORBITOBJECT_H_ */
