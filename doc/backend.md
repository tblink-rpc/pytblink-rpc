
Two backend implementations are currently provided: Python and C++. 
Other environment integrations use these backends as-is, or with minor 
logic on top:
- SysV DPI     -- SystemVerilog wrapper and some custom phasing
- Vlog VPI     -- System tasks and some custom phasing
- Zephyr Cosim -- Effectively as-is
- SystmeC      -- Custom phasing

- Endpoints are symmetrical. The assumption is that an environment 
  establishes and endpoint, the connects that endpoint to 
  another -- typically by launching the other environment and
  having that environment connect back.
  
- An environment has a connect problem if the paired environment
does not provide an API export for one or more imports.

- Probably best if initialization process is always the same
  - Launching side
    - Starts peer
    - Waits for connection
    - Sends 'Hello'
    - Waits for 'HelloAck'
    - Sends API-definition information to peer
    - Accepts API-definition information from peer
    - Sends build-complete message to peer
    - Waits for build-complete from peer
    - Runs connect-time code
    - Sends connect-complete message to peer
    - Waits for connect-complete meesage from peer
    - Begins run-time behavior
    - ...
    - Sends run-complete message (?)
    
  - Launched side
    - Connects to peer
    - Waits for 'Hello' message
    - Sends 'HelloAck'
    - Sends API-definition information to peer
    - Accepts API-definition information from peer
    - Sends build-complete message to peer
    - Waits for build-complete message from peer
    - Runs connect-time code
    - Sends connect-complete message to peer
    - Waits for connect-complete meesage from peer
    - ...
    - Sends run-complete message (?)
    
   - TbLink manager should provide specific support for awaiting messages
   
   - Endpoints have a set of pre-defined services provided
     - Time
     - Time-based callback
   - This information provided with launch

  - Connecting environment waits for InitializationReq (this is a 'hello' message)
  - 
  
# Defining Bundles, APIs, and Object Factories
- Process is:
  - Create element
  - Create sub-elements (as needed)
  - Populate element
  - Register populated element
  
- Global/static   -- registered with ITbLink
- Static-instance -- registered with a single endpoint
- Object          -- factory registered with ITbLink. Objects belong to an endpoint
  
- Assume API/bundle will be used in a single role
  - Global/static   -- singleton
  - Static-instance -- may have multiple instances identified with instance names
  - Object          -- Effectively anonymous. Dynamic creation, operation, deletion
  
# Calling Methods
- Methods are registered within the API of which they are a member
- Methods are identified with an ID corresponding to their index within the container
- Import-API methods are invoked on an endpoint
  - Pass API handle
  - Pass method ID
  - Pass ParamValVector
  - Accept return ParamVal
- Import APIs implement methods to 
  - Pack param values
  - 
- Default association policy is for Import API to associate
  itself with an endpoint on first call (across envs)
 

