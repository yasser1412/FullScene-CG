//
// Created by ahmad on 5/13/20.
//

#include "../include/texture.hpp"
#include "../include/imageloader.h"

GLuint loadTexture(Image* image) {
    GLuint textureId;
    glGenTextures(1, &textureId); //Make room for our texture
    glBindTexture(GL_TEXTURE_2D, textureId); //Tell OpenGL which texture to edit
    //Map the image to the texture
    glTexImage2D(GL_TEXTURE_2D,                //Always GL_TEXTURE_2D
                 0,                            //0 for now
                 GL_RGB,                       //Format OpenGL uses for image
                 image->width, image->height,  //Width and height
                 0,                            //The border of the image
                 GL_RGB, //GL_RGB, because pixels are stored in RGB format
                 GL_UNSIGNED_BYTE, //GL_UNSIGNED_BYTE, because pixels are stored
            //as unsigned numbers
                 image->pixels);               //The actual pixel data
    return textureId; //Returns the id of the texture
}

void drawFloorTexture(GLuint textID){
    //floor
    glPushMatrix();
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, textID);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    glBegin(GL_QUADS);

    glNormal3f(0.0,-1.0,0.0);
    glTexCoord2f(0.0f, 0.0f);


    glVertex3f(-10,-3,10);
    glTexCoord2f(5.0f,  0.0f);

    glVertex3f(10,-3,10);
    glTexCoord2f(5.0f,  20.0f);

    glVertex3f(10,-3,-10);
    glTexCoord2f(0.0f, 20.0f);

    glVertex3f(-10,-3,-10);
    glEnd();
    glDisable(GL_TEXTURE_2D);

    glPopMatrix();
}
