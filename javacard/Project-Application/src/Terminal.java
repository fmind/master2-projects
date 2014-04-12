import javax.smartcardio.CardException;

import sm.appli.CryptoEngine;
import sm.appli.CryptoInterface;

public class Terminal {

	/**
	 * Main class
	 * 
	 * @note uncomment the sample for unit testing
	 * @param args
	 * @throws CardException
	 */
	public static void main(String[] args) throws CardException {
		// wallet initialization
		CryptoEngine crypto = new CryptoEngine();
		crypto.init();
		crypto.selectApplet((short) 0x06);
		
		// interface initialization
		CryptoInterface iface = new CryptoInterface();
		iface.setEngine(crypto);
		
		// launch app
		iface.run();
		
		/* nominal sample */
		/*
		// etudiant: 65 74 75 64 69 61 6E 74
		// salut ebu: 73 61 6C 75 74 20 65 62 75
		// masterssic: 6D 61 73 74 65 72 73 73 69 63
		
		System.out.println("SetKeySm(etudiant)");
		crypto.setSymKey("etudiant");
		System.out.println("");
		
		System.out.println("EncryptDES(etudiant)");
		String res1 = crypto.encryptDES("etudiant");
		System.out.println("RESULT=" + res1);
		System.out.println("");
		
		System.out.println("EncryptDES(salut ebu)");
		String res2 = crypto.encryptDES("salut ebu");
		System.out.println("RESULT=" + res2);
		System.out.println("");
		
		System.out.println("EncryptDES(masterssic)");
		String res3 = crypto.encryptDES("masterssic");
		System.out.println("RESULT=" + res3);
		System.out.println("");
		
		System.out.println("DecryptDES(31 EA EB A1 0E 85 5E F0)");
		String res4 = crypto.decryptDES("31 EA EB A1 0E 85 5E F0");
		System.out.println("RESULT=" + res4);
		System.out.println("");
		
		System.out.println("DecryptDES(CC C2 D6 CD 46 FE 95 3B 7F 35 33 53 BA 4C 1F E7)");
		String res5 = crypto.decryptDES("CC C2 D6 CD 46 FE 95 3B 7F 35 33 53 BA 4C 1F E7");
		System.out.println("RESULT=" + res5);
		System.out.println("");
		
		System.out.println("DecryptDES(EE 31 D1 6F C5 73 55 85 7B 07 28 08 F2 6F AA 6F)");
		String res6 = crypto.decryptDES("EE 31 D1 6F C5 73 55 85 7B 07 28 08 F2 6F AA 6F");
		System.out.println("RESULT=" + res6);
		System.out.println("");
		
		crypto.end();
		*/
		/* end nominal sample */
		
		/* error sample */
		// no key set
		/*
		System.out.println("EncryptDES(etudiant) [no key set]");
		crypto.encryptDES("etudiant");
		*/
		// key length invalid
		/*
		System.out.println("SetKeySm(etudiantetudiant)");
		crypto.setSymKey("etudiantetudiant");
		*/
		// message empty
		/*
		System.out.println("EncryptDES()");
		crypto.encryptDES("");
		*/
		/* end error sample */
	}
}
