"""This module defines MyPlugIn, a custom plugin for the nifti application within the BrkRaw framework.
The MyPlugIn class extends the BasePlugin class and is tailored to enhance the functionality of
BrkRaw's conversion process by allowing specific customizations for NIfTI conversions.

Key Features:
- Allows custom handling of data objects, affine transformations, and NIfTI headers based on
  specific scan, reconstruction, or file data.
- Includes methods for inspecting data compatibility and setting parameters based on the provided
  PvObj instances (PvScan, PvReco, PvFiles).
- Supports the integration of additional processing needs by overriding mandatory and optional methods.

The plugin architecture is designed to facilitate easy additions and modifications to the data processing
pipeline, making it adaptable to various research requirements.

Author: SungHo Lee
Created: 2024-04-30
"""


from __future__ import annotations
from brkraw.app.tonifti import BasePlugin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from numpy.typing import NDArray
    from typing import Union, Optional
    from nibabel.nifti1 import Nifti1Header
    from brkraw.app.tonifti import PvScan, PvReco, PvFiles
    

class MyPlugIn(BasePlugin):
    """ Boilerplate code for a plugin for the nifti app in BrkRaw.
    
    The BasePlugin class extends the Scan class in brkraw.api.data. Refer to any compatible methods from
    brkraw.api.data.scan.Scan for further guidance.
    
    Mandatory methods that must be implemented:
        - get_dataobj(self, reco_id: Optional[int] = None) -> NDArray:
            This method returns a data object in numpy ndarray format. Include custom code for data processing as needed.
            'reco_id' is required when accessing data under the pdata folder (such as '2dseq').
            
        - get_affine(self, reco_id: Optional[int] = None, subj_type: Optional[str] = None, subj_position: Optional[str] = None) -> NDArray:
            This method returns an affine matrix. Include custom rotations as necessary.
            'reco_id', 'subj_type', and 'subj_position' are optional parameters to support type and position overrides.
            
        - get_nifti1header(self, reco_id: Optional[int] = None) -> Nifti1Header:
            This method returns a modified NIfTI header. Make any necessary updates to the NIfTI Header here.
        
    Optional internal methods:
        - _inspect(self):
            This method should be implemented to check whether the given data is compatible with the plugin.
        - _set_params(self):
            This method should be implemented to set parameter data or map binary files to class attributes.
    """
    
    def __init__(self, pvobj: Union['PvScan', 'PvReco', 'PvFiles'],
                 # --- start of custom arguments ---
                 option: Optional[bool],
                 # ---  end of custom arguments  ---
                 **kwargs
                 ) -> None:
        """Initialize the plugin with a PvObj class instance.
        
        Args:
            pvobj (PvScan | PvReco | PvFiles): Primitive class for PvObj (PvStudy is not supported).
            option (bool): If true, multiply dataobj by 2
        """
        super().__init__(pvobj, **kwargs)
        # --- start of mapping custom argumentss ---
        self.option = option
        # ---  end of mapping custom arguments  ---
        self._inspect()
        self._set_params()
        
    def _inspect(self):
        """Inspect the provided data to ensure compatibility with this plugin.
        
        Example checks might include verifying parameters in 'acqp', 'method', and 'visu_pars' files.
        """
        pass
    
    def _set_params(self):
        """Set parameter values or file objects as attributes of this class.
        
        Access parameter files and read necessary binary data.
        """
        self.acqp = self.pvobj.acqp
        self.method = self.pvobj.method
        self.visu_pars = self.pvobj.get_visu_pars()  # this will get visu_pars from first pdata available to the dataset
        
        with self.pvobj.get_fid() as f:
            self.fid = f.read()
        with self.pvobj.get_2dseq() as f:  # this will get 2dseq from first pdata available to the dataset
            self.dataarray = f.read()
        
        
    def get_dataobj(self, reco_id: Optional[int] = None) -> NDArray:
        """Retrieve the data object, optionally filtered by reco_id.

        Args:
            reco_id (Optional[int]): Specifies the reconstruction ID to filter the data.

        Returns:
            NDArray: The data object as a numpy ndarray.
        """
        dataobj = super().get_dataobj(scanobj=self, 
                                      reco_id=reco_id)
        if self.option:
            dataobj *= 2
        return dataobj
    
    def get_affine(self, reco_id:Optional[int]=None, 
                   subj_type:Optional[str]=None, 
                   subj_position:Optional[str]=None) -> NDArray:
        """Retrieve the affine transformation matrix.

        Args:
            reco_id (Optional[int]): Reconstruction ID if specific data access is needed.
            subj_type (Optional[str]): Subject type for custom processing.
            subj_position (Optional[str]): Subject position for custom processing.

        Returns:
            NDArray: Affine transformation matrix.
        """
        return super().get_affine(scanobj=self, 
                                  reco_id=reco_id, 
                                  subj_type=subj_type, 
                                  subj_position=subj_position)
    
    def get_nifti1header(self) -> Nifti1Header:
        """Retrieve the NIfTI header updated as necessary for this plugin.

        Returns:
            Nifti1Header: The updated NIfTI header.
        """
        return super().get_nifti1header(self)