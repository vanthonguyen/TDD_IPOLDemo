"""
3D Geometric Analysis of Tubular Objects based on Surface Normal Accumulation
demo editor: Bertrand Kerautret
"""

from lib import base_app, build, http, image, config
from lib.misc import app_expose, ctime
from lib.base_app import init_app

import cherrypy
from cherrypy import TimeoutError
import os.path
import shutil
import time

class app(base_app):
    """ template demo app """

    title = "3D Geometric Analysis of Tubular Objects based on Surface Normal Accumulation: Online Demonstration"
    xlink_article = 'http://www.ipol.im/'
    xlink_src = 'http://www.ipol.im/pub/pre/67/gjknd_1.1.tgz'
    dgtal_src = 'https://github.com/kerautret/DGtal.git'
    demo_src_filename  = 'gjknd_1.1.tgz'
    demo_src_dir = 'SingleKnotsDetection'


    input_nb = 1 # number of input images
    input_max_pixels = 4096 * 4096 # max size (in pixels) of an input image
    input_max_weight = 1 * 4096 * 4096 # max size (in bytes) of an input file
    input_dtype = '3x8i' # input image expected data type
    input_ext = '.png'   # input image expected extension (ie file format)
    is_test = False       # switch to False for deployment
    commands = []
    def __init__(self):
        """
        app setup
        """
        # setup the parent class
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_app.__init__(self, base_dir)

        # select the base_app steps to expose
        # index() is generic
        app_expose(base_app.index)
        app_expose(base_app.input_select)
        app_expose(base_app.input_upload)
        # params() is modified from the template
        app_expose(base_app.params)
        # run() and result() must be defined here




        

    def build(self):
        """
        program build/update
        """
        # store common file path in variables
        # tgz_file = self.dl_dir + self.demo_src_filename
        # prog_names = ["dll_decomposition", "dll_sequence", "testBoundaries", \
        # 			  "testDecomposition", "testOtsu"]
        # prog_bin_files = []

        # for f in prog_names:
        #     prog_bin_files.append(self.bin_dir+ f)

        # log_file = self.base_dir + "build.log"
        # # get the latest source archive
        # print ("Starting download \n")
        # build.download(self.xlink_src, tgz_file)
        # print ("download ended... \n")
        # # test if the dest file is missing, or too old
        # if (os.path.isfile(prog_bin_files[0])
        #     and ctime(tgz_file) < ctime(prog_bin_files[0])):
        #     cherrypy.log("not rebuild needed",
        #                  context='BUILD', traceback=False)
        # else:
        #     # extract the archive
        #     build.extract(tgz_file, self.src_dir)
        #     # build the program
        #     build.run("cd %s; git clone %s" %(self.src_dir) %("https://github.com/kerautret/DGtal.git"))
        #     build.run("cd %s ; mkdir build; cmake .. -DCMAKE_BUILD_TYPE=Release; make -j 4" %(self.src_dir + "DGtal"))
            
        #     #build.run("mkdir %s;  " %(self.src_dir+"gjknd_1.1/build"), \
        #    #            						 stdout=log_file)
        #    # build.run("cd %s; cmake .. ; make -j 4" %(self.src_dir + \
        #     #							"gjknd_1.1/build"),stdout=log_file)

        #     # save into bin dir
        #     if os.path.isdir(self.bin_dir):
        #         shutil.rmtree(self.bin_dir)
        #     os.mkdir(self.bin_dir)
        #     for i in range(0, len(prog_bin_files)) :
        #         shutil.copy(self.src_dir + os.path.join("gjknd_1.1/build/src", \
        #         			prog_names[i]), prog_bin_files[i])

        #     # cleanup the source dir
        #     shutil.rmtree(self.src_dir)

        return



    def input_select_callback(self, fnames):
        '''
        Implement the callback for the input select to
        process the non-standard input
        '''         
        self.cfg['meta']['is3d'] = True
        if self.cfg['meta']['is3d'] :
            baseName = (fnames[0])[0:-4]
            #radius = (fnames[0])[-7:-4]
            radius = 50
            self.cfg['meta']['rad'] = float(radius)
            shutil.copy(self.input_dir +baseName+".off",
                        self.work_dir + 'inputVol_0.off')        
        self.cfg.save()





    @cherrypy.expose
    @init_app
    def params(self, newrun=False, msg=None):
        """Parameter handling (optional crop)."""

        # if a new experiment on the same image, clone data
        if newrun:
             oldPath = self.work_dir + 'inputVol_0.off'
             self.clone_input()
             shutil.copy(oldPath, self.work_dir + 'inputVol_0.off')

        # save the input image as 'input_0_selection.png', the one to be used
        img = image(self.work_dir + 'input_0.png')
        img.save(self.work_dir + 'input_0_selection.png')
        img.save(self.work_dir + 'input_0_selection.pgm')

        # initialize subimage parameters
        self.cfg['param'] = {'x1':-1, 'y1':-1, 'x2':-1, 'y2':-1}
        self.cfg.save()
        return self.tmpl_out('params.html')

   



    @cherrypy.expose
    @init_app
    def wait(self, **kwargs):
        """
        params handling and run redirection
        """

        # save and validate the parameters
        try:
            self.cfg['param']['radius'] = kwargs['radius']

            self.cfg.save()
        except ValueError:
            return self.error(errcode='badparams',
                              errmsg="The parameters must be numeric.")

        http.refresh(self.base_url + 'run?key=%s' % self.key)
        return self.tmpl_out("wait.html")

    @cherrypy.expose
    @init_app
    def run(self):
        """
        algo execution
        """

        # read the parameters
        #print self.cfg['param']

        #shutil.copy(self.input_dir +self.cfg['meta']['basename']+".vol",
        #            self.work_dir + 'inputVol_0.vol')        
        #shutil.copy(self.input_dir +self.cfg['meta']['basename']+".sdp",
        #            self.work_dir + 'inputVol_0.sdp')        
                 
        # run the algorithm
        #self.commands = ""

        try:
            self.run_algo(self)
        except TimeoutError:
            return self.error(errcode='timeout')
        except RuntimeError:
            return self.error(errcode='runtime',
                              errmsg="Something went wrong with the program.")
        except ValueError:
            return self.error(errcode='badparams',
                              errmsg="The parameters given produce no contours,\
                              		  please change them.")

        http.redir_303(self.base_url + 'result?key=%s' % self.key)

        # # archive
        # if self.cfg['meta']['original']:
        #     ar = self.make_archive()
        #     ar.add_file("input_0.png", "original.png", info="uploaded")
        #     ar.add_file("output.txt", info="output.txt")
        #     ar.add_file("commands.txt", info="commands.txt")
        #     ar.add_file(typeprimitive+"_out_input_0.png", info="output")
        #     ar.add_info({"type primitive": typeprimitive})
        #     ar.add_info({"use black background": b})

        #     ar.save()

        return self.tmpl_out("run.html")






    def run_algo(self, params):
        """
        the core algo runner
        could also be called by a batch processor
        this one needs no parameter
        """
        #radius = self.cfg['param']['radius']
        
        f = open(self.work_dir+"output.txt", "w")
        fInfo = open(self.work_dir+"info.txt", "w")
        command_args = 'onestep.sh ' +  self.work_dir + "inputVol_0.off"

        p = self.run_shell(command_args, stderr=fInfo, env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=120)
        fInfo.close()
        f.close()
        return

    @cherrypy.expose
    @init_app
    def result(self, public=None):
        """
        display the algo results
        """
        return self.tmpl_out("result.html",
                             height=500)



    def runCommand(self, command, stdOut=None, stdErr=None):
        """
        Run command and update the attribute list_commands
        """
        p = self.run_proc(command, stderr=stdErr, stdout=stdOut, \
        				  env={'LD_LIBRARY_PATH' : self.bin_dir})
        self.wait_proc(p, timeout=self.timeout)
        # transform convert.sh in it classic prog command (equivalent)
        # command_to_save = ' '.join(['"' + arg + '"' if ' ' in arg else arg
        #          for arg in command ])
        #if comp is not None:
        #    command_to_save += comp
        #self.list_commands +=  command_to_save + '\n'
        #sreturn command_to_save


    def run_shell(self, args, stdin=None, stdout=None, stderr=None, env=None):
        """
        execute a sub-process from the 'tmp' folder
        """

        if env is None:
            env = {}
        # update the environment
        newenv = os.environ.copy()
        # add local environment settings
        newenv.update(env)

        # TODO clear the PATH, hard-rewrite the exec arg0
        # TODO use shell-string execution

        # Add PATH in configuration
        path = self.bin_dir
        if 'PATH' in env:
            path = path + ":" + env['PATH']
        # Check if there are extra paths (for example, for MATLAB)
        if 'server.extra_path' in cherrypy.config:
            path = path + ":" + cherrypy.config['server.extra_path']
        #
        newenv.update({'PATH' : path})

        # run
        return Popen(args, stdin=stdin, stdout=stdout, stderr=stderr,
                     env=newenv, cwd=self.work_dir, shell=True)


