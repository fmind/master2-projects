package sm.appli;

import javax.smartcardio.CardException;

public class AppliClient4_Terminal {

	public static void main(String[] args) throws CardException, CommandError {
		// wallet initialization
		Wallet wallet = new Wallet();
		wallet.init();
		//wallet.selectAppletWithoutPin();
		wallet.selectAppletWithPin();
		
		// interface initialization
		CLIInterface iface = CLIInterface.getInstance();
		iface.setWallet(wallet);
		
		// launch app
		iface.run();

		// app termination
		wallet.end();
		
		/* nominal sample */
		/*
		System.out.println("BALANCE=" + wallet.getBalance());
		System.out.println("");

		System.out.println("Crediting of your card (balance+100) ...");
		wallet.credit(100);
		System.out.println("BALANCE=" + wallet.getBalance());
		System.out.println("");
		
		System.out.println("Debiting of your card (balance-4) ...");
		wallet.debit(4);
		System.out.println("BALANCE=" + wallet.getBalance());
		System.out.println("");
		
		System.out.println("Reseting the balance of your card (balance=0) ...");
		wallet.reset();
		System.out.println("BALANCE=" + wallet.getBalance());
		System.out.println("");
		
		wallet.end();
		*/
		/* end nominal sample */
		
		/* error sample */
		//try {
			// crediting too much
			/*
			System.out.println("Crediting of your card (balance+101) ...");
			wallet.credit(101);
			 */
			// debiting too much
			/*
			System.out.println("Debiting of your card (balance-101) ...");
			wallet.credit(100);
			wallet.credit(100);
			wallet.debit(101);
			*/
			// maximum wallet value
			/*
			System.out.println("Crediting of your card (balance+100*501) ...");
			for (int i=0; i<500; i++) {
				System.out.println("BALANCE=" + wallet.getBalance());
				wallet.credit(100);
			}
			*/
			// negative balance
			/*
			System.out.println("Debiting of your card (0-10) ...");
			wallet.debit(10);
			*/
			// pin not long enough
			//wallet.verify("123");
			// pin too long
			//wallet.verify("12345");
			// pin not a number
			//wallet.verify("11aa");
		/*
		} catch (CommandError err) {
			System.err.println(err);
			System.out.println("Reseting the balance of your card (balance=0) ...");
			wallet.reset();
			wallet.end();
		}
		*/
		
		/* end error sample */
	}
}
