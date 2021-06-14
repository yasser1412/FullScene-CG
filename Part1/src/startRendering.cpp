//
// Created by ahmad on 5/13/20.
//

#include "../include/startRendering.hpp"
#include <iostream>
#include "../include/imageloader.h"
#include <GL/glut.h>
#include "../include/texture.hpp"
// RGBA
GLfloat light_ambient[] = { 0.0, 0.0, 0.0, 0.0 };
GLfloat light_diffuse[] = { 0.5, 0.5, 0.5,1.0 };
GLfloat light_specular[] = {1.0, 1.0, 1.0, 1.0 };
// x , y, z, w
GLfloat light_position[] = {0.5,5.0, 0.0, 1.0 };
GLfloat lightPos1[] = {-0.5,-5.0,-2.0, 1.0 };
// Material Properties
GLfloat mat_amb_diff[] = {0.643, 0.753, 0.934, 1.0 };
GLfloat mat_specular[] = { 0.0, 0.0, 0.0, 1.0 };
GLfloat shininess[] = {100.0 };

//Initializes 3D rendering
void initRendering(const char* bmbImg, GLuint & textureID){
    // Loading a Texture
    Image *image = loadBMP(bmbImg);
    textureID = loadTexture(image);
    delete image;

   // Lighting and Rendering Stuff

   // Turn on the power
   glEnable(GL_LIGHTING);

   // Flip light switch
   glEnable(GL_LIGHT0);
   glEnable(GL_LIGHT1);

   // assign light parameters
   glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
   glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
   glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
   glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient);
   glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse);
   glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular);

   // Material Properties
   glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, mat_amb_diff);
   glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
   glMaterialfv(GL_FRONT, GL_SHININESS, shininess);
   GLfloat lightColor1[] = {1.0f, 1.0f,  1.0f, 1.0f };
   // Lighting Properties
   glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1);
   glLightfv(GL_LIGHT1, GL_POSITION, lightPos1);
   glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor1);
   glEnable(GL_NORMALIZE);

   //Enable smooth shading
   glShadeModel(GL_SMOOTH);

   // Enable Depth buffer
   glEnable(GL_DEPTH_TEST);
}