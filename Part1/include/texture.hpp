//
// Created by ahmad on 5/13/20.
//

#ifndef FULL_SCENE_ANIMATION_TEXTURE_HPP
#define FULL_SCENE_ANIMATION_TEXTURE_HPP

#include "../include/imageloader.h"
#include <GL/glut.h>

GLuint loadTexture(Image* image);  // Loads A given Texture using Image Object and returns it`s id
void drawFloorTexture(GLuint textID);  // Draw a floor from a bitmap image


#endif //FULL_SCENE_ANIMATION_TEXTURE_HPP
