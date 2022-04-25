// SPDX LIS necessary 0.6.8 onwards
// SPDX-License-Identifier: MIT
// define solidity version at top always. ^0.60 means all 0.6 versions. 0.6 means just 0.6.
pragma solidity >= 0.6.0 <0.9.0;
// define contract-- like a class in OOP
pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoriteNumber;

    // This is a comment!
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public {
    // functions or methods self ocntained modules that execute tasks
    function store(uint256 _favoriteNumber) public {
        // default scope for state variables is internal
        // internal - inside contract only
        // external - outside contraxt only
        // public - both, by anyone
        // private - restricive, only current contract not derived
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
