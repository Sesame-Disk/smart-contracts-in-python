// SPDX LIS necessary 0.6.8 onwards
// SPDX-License-Identifier: MIT
// define solidity version at top always. ^0.60 means all 0.6 versions. 0.6 means just 0.6.
pragma solidity >= 0.6.0 <0.9.0;
// define contract-- like a class in OOP

contract SimpleStorage {
    // unsigned integer 256 bits; initialized to 0
    uint256 favoriteNumber;
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    People [] public people;
    
    mapping(string => uint256) public nameToFavNum;
    
    People public person = People({favoriteNumber: 2, name: "Umar"});
    // functions or methods self ocntained modules that execute tasks
    function store(uint256 _favoriteNumber) public {
        // default scope for state variables is internal
        // internal - inside contract only
        // external - outside contraxt only
        // public - both, by anyone
        // private - restricive, only current contract not derived
        favoriteNumber = _favoriteNumber;
    }
    function retreive() public view returns(uint256){
        return favoriteNumber;
    }
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        //people.push(People({favoriteNumber : _favoriteNumber, name: _name}));
        people.push(People(_favoriteNumber , _name));
        nameToFavNum[_name] = _favoriteNumber;
    }
}
