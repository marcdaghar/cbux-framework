// SPDX-License-Identifier: CC-BY-SA-4.0
pragma solidity ^0.8.19;

contract UnitX {
    struct Devis {
        string id;
        string client;
        uint256 date;
        uint256 montantX;
        uint256 tauxConversion;
        uint256 montantEUR;
        bool estValide;
    }
    
    struct Facture {
        string id;
        string devisRef;
        uint256 dateEmission;
        uint256 montantX;
        uint256 tauxConversion;
        uint256 montantEURLegal;
        bool estPayee;
    }
    
    mapping(string => Devis) public devis;
    mapping(string => Facture) public factures;
    uint256 public tauxJournalier;
    uint256 public derniereMiseAJour;
    
    uint256 public alpha = 500;
    uint256 public beta = 300;
    uint256 public gamma = 200;
    
    event TauxMisAJour(uint256 taux, uint256 timestamp);
    event DevisCree(string id, uint256 montantX, uint256 montantEUR);
    event FactureEmise(string id, uint256 montantX, uint256 montantEURLegal);
    event FacturePayee(string id);
    
    constructor() {
        tauxJournalier = 27980;
        derniereMiseAJour = block.timestamp;
    }
    
    function mettreAJourTaux(uint256 _taux) external {
        require(_taux > 0, "Taux invalide");
        tauxJournalier = _taux;
        derniereMiseAJour = block.timestamp;
        emit TauxMisAJour(_taux, block.timestamp);
    }
    
    function getTaux() public view returns (uint256) {
        return tauxJournalier;
    }
    
    function creerDevis(string memory id, string memory client, uint256 montantX) external {
        require(!devis[id].estValide, "Devis existe deja");
        uint256 montantEUR = montantX * tauxJournalier / 1000;
        devis[id] = Devis({
            id: id,
            client: client,
            date: block.timestamp,
            montantX: montantX,
            tauxConversion: tauxJournalier,
            montantEUR: montantEUR,
            estValide: true
        });
        emit DevisCree(id, montantX, montantEUR);
    }
    
    function convertirXEnEUR(uint256 montantX) public view returns (uint256) {
        return montantX * getTaux() / 1000;
    }
    
    function convertirEUREnX(uint256 montantEUR) public view returns (uint256) {
        return montantEUR * 1000 / getTaux();
    }
}
