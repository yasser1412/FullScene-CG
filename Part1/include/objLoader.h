#ifndef OBJ_LOADER_H
#define OBJ_LOADER_H
#include "../include/glm.h"

/*Wavefront object of extension ".obj"
*/
class Model
{
private:
    char *path;
    GLMmodel *model;

public:
    //Model Constructor
    Model(char *path);

    /*Read new model from a Wavefront.OBJ file.
    * 
    * path: realtive path of obj file.
    * 
    * RETRUN: Void
    */
    void load(char *path);

    /*Render the model to current position.
    *
    * RETRUN: Void
    */
    void draw();

    /*Scale model by given factor.
    *
    * factor: scale factor (0.5 = half as large, 2.0 = twice as large).
    * 
    * RETRUN: Void
    */
    void scale(float factor);
};
#endif