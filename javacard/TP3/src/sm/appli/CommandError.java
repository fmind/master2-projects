package sm.appli;

public class CommandError extends Error {
	
	public CommandError(int code, String msg) {
		super("[CODE: " + Integer.toHexString(code) + "] " + msg);
	}
}
