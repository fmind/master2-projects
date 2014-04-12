package sm.appli;

public class CommandError extends Error {
	private String message;
	
	/**
	 * Constructor with error and message code
	 * 
	 * @param code
	 * @param msg
	 */
	public CommandError(int code, String msg) {
		super("[CODE: " + Integer.toHexString(code) + "] " + msg);
		this.message = "[CODE: " + Integer.toHexString(code) + "] " + msg;
	}
	
	/**
	 * Convert to String
	 */
	public String toString() {
		return message;
	}
}
